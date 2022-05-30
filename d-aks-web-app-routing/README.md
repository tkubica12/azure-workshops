# Demo - ASK managed ingress solution with Web Application Routing
In this demo we will look into managed solution for Ingress using NGINX controller, DNS automation, certificate store using Key Vault and integration with Open Service Mesh for E2E encryption. 



```bash
# Install the aks-preview extension
az extension add --name aks-preview

# Update the extension to make sure you have the latest version installed
az extension update --name aks-preview

az group create -n akswebrouting -l westeurope
az aks create -n akswebrouting -g akswebrouting -c 1 -x -k 1.23.5 --network-plugin azure -s Standard_B4ms --enable-addons web_application_routing,open-service-mesh,azure-keyvault-secrets-provider
az aks get-credentials --admin --overwrite-existing -n akswebrouting -g akswebrouting
kubectl create namespace myweb
osm namespace add myweb


az keyvault set-policy --name myapp-contoso --object-id <WEB_APP_ROUTING_MSI_OBJECT_ID>  --secret-permissions get --certificate-permissions get


az group delete -n akswebrouting -y



--dns-zone-resource-id

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
```