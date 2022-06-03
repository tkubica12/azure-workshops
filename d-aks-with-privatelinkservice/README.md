# Demo - using AKS with Private Link Service eg. in SaaS provider scenario
In this demo we will create AKS cluster and use annotations to configure Private Link Service. This can be used to provide private connectivity to applications running in AKS for different VNETs including different tenants eg. when SaaS provider runs AKS in their subscription providing private network access to customers in their subscriptions.

```bash
# Create AKS
az group create -n akspls -l westeurope
az network vnet create -n aksplsvnet -g akspls --address-prefixes 10.88.0.0/16 
az network vnet subnet create -n aks -g akspls --vnet-name aksplsvnet --address-prefix 10.88.0.0/22
az network vnet subnet create -n lb -g akspls --vnet-name aksplsvnet --address-prefix 10.88.4.0/24
az network vnet subnet create -n privatelinks -g akspls --vnet-name aksplsvnet --address-prefix 10.88.5.0/24
az identity create -n aksplmidentity -g akspls
az role assignment create --assignee $(az identity show -n aksplmidentity -g akspls --query principalId -o tsv) --role "Contributor" -g akspls
az aks create -n akspls -g akspls -c 1 -x -k 1.23.5 --network-plugin azure -s Standard_B2s \
    --vnet-subnet-id $(az network vnet subnet show -n aks  -g akspls --vnet-name aksplsvnet --query id -o tsv) \
    --assign-identity $(az identity show -n aksplmidentity -g akspls --query id -o tsv) \
    --assign-kubelet-identity $(az identity show -n aksplmidentity -g akspls --query id -o tsv)
az aks get-credentials --admin --overwrite-existing -n akspls -g akspls

# Install NGINX ingress with annotations to enable PLS
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm upgrade -i ingress-nginx ingress-nginx/ingress-nginx \
  --create-namespace \
  --namespace ingress \
  -f values.yaml

# Install and expose app
kubectl apply -f app.yaml
```

## Test as Azure customer - project provider app to customer VNET using Private Endpoint
```bash
# Create VNET and VM (no I am on purpose use the same ip addresing to demonstrate there is no need to coordinate on ranges or anything)
az group create -n client -l westeurope
az network vnet create -n clientvnet -g client --address-prefixes 10.88.0.0/16 
az network vnet subnet create -n vm -g client --vnet-name clientvnet --address-prefix 10.88.0.0/24
az storage account create -n tomasclientstorage123 -g client
az vm create -n clientvm \
  -g client \
  --size Standard_B1s \
  --image UbuntuLTS \
  --vnet-name clientvnet \
  --subnet vm \
  --authentication-type password \
  --admin-username tomas \
  --admin-password Azure12345678 \
  --nsg "" \
  --public-ip-address "" \
  --boot-diagnostics-storage tomasclientstorage123

# Create private endpoint for Ingress
az network private-endpoint create \
    --connection-name myConnection \
    -n myPrivateEndpoint \
    --private-connection-resource-id $(az network private-link-service show -g MC_akspls_akspls_westeurope -n myservice --query id -o tsv) \
    -g client \
    --subnet vm \
    --vnet-name clientvnet  

# Create private endpoint for direct service
az network private-endpoint create \
    --connection-name myConnectionDirect \
    -n myPrivateEndpointDirect \
    --private-connection-resource-id $(az network private-link-service show -g MC_akspls_akspls_westeurope -n myservicedirect --query id -o tsv) \
    -g client \
    --subnet vm \
    --vnet-name clientvnet  

# Get Private Endpoint IP for Ingress 
az network nic show \
  --ids $(az network private-endpoint show -n myPrivateEndpoint -g client --query networkInterfaces[0].id -o tsv) \
  --query ipConfigurations[0].privateIpAddress -o tsv

# Get Private Endpoint IP for Direct service 
az network nic show \
  --ids $(az network private-endpoint show -n myPrivateEndpointDirect -g client --query networkInterfaces[0].id -o tsv) \
  --query ipConfigurations[0].privateIpAddress -o tsv

# Test access from VM
az serial-console connect -n clientvm -g client 
curl 10.88.0.5
curl 10.88.0.6 -H 'Host:myapp.demo'
```

## Test with Azure Front Door Premium
```bash
# Create Front Foor
az afd profile create --profile-name tomasafd -g akspls --sku Premium_AzureFrontDoor

# Create endpoint
az afd endpoint create -g akspls \
    --endpoint-name tomasafd \
    --profile-name tomasafd

# Create Origin group for direct service
az afd origin-group create -g akspls  \
  --origin-group-name originsDirect \
  --profile-name tomasafd \
  --probe-request-type GET \
  --probe-protocol Http \
  --probe-interval-in-seconds 120 \
  --probe-path / \
  --sample-size 4 \
  --successful-samples-required 3 \
  --additional-latency-in-milliseconds 50

# Create origin with private link for direct service
az afd origin create -g akspls  \
    --host-name 10.88.4.4 \
    --profile-name tomasafd \
    --origin-group-name originsDirect \
    --origin-name myappdirect \
    --origin-host-header 10.88.4.4 \
    --enabled-state Enabled \
    --enable-private-link true \
    --private-link-location westeurope \
    --private-link-resource $(az network private-link-service show -g MC_akspls_akspls_westeurope -n myservicedirect --query id -o tsv) \
    --private-link-request-message "myrequest1"

# Approve private connection for direct service
az network private-endpoint-connection approve --id $(
  az network private-endpoint-connection list \
    --id $(az network private-link-service show -g MC_akspls_akspls_westeurope -n myservicedirect --query id -o tsv) \
    --query "[?properties.privateLinkServiceConnectionState.description == 'myrequest1'].id" -o tsv)

# Create routing rule
az afd route create -g akspls \
  --endpoint-name tomasafd \
  --profile-name tomasafd \
  --supported-protocols Https \
  --forwarding-protocol HttpOnly \
  --route-name myappdirect \
  --https-redirect Enabled \
  --patterns-to-match  "/direct/*" \
  --origin-path "/" \
  --origin-group originsDirect \
  --link-to-default-domain Enabled

# Test connection
export url=https://$(az afd endpoint show -g akspls --endpoint-name tomasafd --profile-name tomasafd --query hostName -o tsv)
curl $url/direct/

# Create Origin group for ingress
az afd origin-group create -g akspls  \
  --origin-group-name originsIngress \
  --profile-name tomasafd \
  --probe-request-type GET \
  --probe-protocol Http \
  --probe-interval-in-seconds 120 \
  --probe-path / \
  --sample-size 4 \
  --successful-samples-required 3 \
  --additional-latency-in-milliseconds 50

# Create origin with private link for ingress
az afd origin create -g akspls  \
    --host-name 10.88.4.4 \
    --profile-name tomasafd \
    --origin-group-name originsIngress \
    --origin-name myappingress \
    --origin-host-header myapp.demo \
    --enabled-state Enabled \
    --enable-private-link true \
    --private-link-location westeurope \
    --private-link-resource $(az network private-link-service show -g MC_akspls_akspls_westeurope -n myservice --query id -o tsv) \
    --private-link-request-message "myrequest1"

# Approve private connection for ingress
az network private-endpoint-connection approve --id $(
  az network private-endpoint-connection list \
    --id $(az network private-link-service show -g MC_akspls_akspls_westeurope -n myservice --query id -o tsv) \
    --query "[?properties.privateLinkServiceConnectionState.description == 'myrequest1'].id" -o tsv)

# Create routing rule
az afd route create -g akspls \
  --endpoint-name tomasafd \
  --profile-name tomasafd \
  --supported-protocols Https \
  --forwarding-protocol HttpOnly \
  --route-name myappingress \
  --https-redirect Enabled \
  --patterns-to-match  "/ingress/*" \
  --origin-path "/" \
  --origin-group originsIngress \
  --link-to-default-domain Enabled

# Test connection
export url=https://$(az afd endpoint show -g akspls --endpoint-name tomasafd --profile-name tomasafd --query hostName -o tsv)
curl $url/ingress/
```