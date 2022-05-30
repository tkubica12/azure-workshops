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
```