# Simple Kubecost demo
Deploy AKS and Kubecost

```bash
# Create Resource Group
az group create -n kubecost -l northeurope 

# Create AKS
az aks create -n kubecost -g kubecost -c 3 -s Standard_B2s -x

# Get credentials
az aks get-credentials -n kubecost -g kubecost --admin

# Deploy services
kubectl apply -f resources.yaml

# Export kubecost token you got from kubecost.com
export KUBECOST_TOKEN="mykey"

# Install Kubecost
kubectl create namespace kubecost
helm repo add kubecost https://kubecost.github.io/cost-analyzer/
helm install kubecost kubecost/cost-analyzer --namespace kubecost --set kubecostToken=$KUBECOST_TOKEN
```

Access kubecost at http://localhost:9090 

```
kubectl port-forward --namespace kubecost deployment/kubecost-cost-analyzer 9090
```