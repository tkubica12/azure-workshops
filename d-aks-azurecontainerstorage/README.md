# AKS with Azure Container Storage

Provision
```bash
az group create -n d-aks-azurecontainerstorage -l westeurope
az aks create -n d-aks-azurecontainerstorage -g d-aks-azurecontainerstorage --node-count 3 --node-vm-size Standard_L8as_v3 -x --zones 1 2 3
az aks nodepool update -g d-aks-azurecontainerstorage --cluster-name d-aks-azurecontainerstorage --name nodepool1 --labels acstor.azure.com/io-engine=acstor

export AKS_MI_OBJECT_ID=$(az aks show -n d-aks-azurecontainerstorage -g d-aks-azurecontainerstorage  --query "identityProfile.kubeletidentity.objectId" -o tsv)
export AKS_NODE_RG=$(az aks show -n d-aks-azurecontainerstorage -g d-aks-azurecontainerstorage  --query "nodeResourceGroup" -o tsv)

az role assignment create --assignee $AKS_MI_OBJECT_ID --role "Contributor" --resource-group "$AKS_NODE_RG"

az aks get-credentials -n d-aks-azurecontainerstorage -g d-aks-azurecontainerstorage --admin --overwrite-existing

az k8s-extension create --cluster-type managedClusters --cluster-name d-aks-azurecontainerstorage -g d-aks-azurecontainerstorage -n acstor --extension-type microsoft.azurecontainerstorage --scope cluster --release-train prod --release-namespace acstor

```

Install demo - this creates storage classes, Azure Container Storage pools and StatefulSet with 3 replicas + for comparison standard StatefulSet with CSI. ConfigMap with fio config files is mapped to each Pod for easy testing.

```bash
helm upgrade -i demo helm/demo

fio --runtime 10 fio/sync-w.ini
```

Connect to different Pods and test performance

```bash
fio --runtime 10 fio/sync-w.ini   # write latency measurement (small block, synchronous)
fio --runtime 10 fio/sync-r.ini   # read latency measurement (small block, synchronous)
fio --runtime 10 fio/async-w.ini  # write IOPS measurement (small block, asynchronous with large iodepth)
fio --runtime 10 fio/async-r.ini  # read IOPS measurement (small block, asynchronous with large iodepth)
fio --runtime 10 fio/large-w.ini  # write throughput measurement (large block, asynchronous with large iodepth)
fio --runtime 10 fio/large-r.ini  # read throughput measurement (large block, asynchronous with large iodepth)
```

Destroy

```bash
az group delete -n d-aks-azurecontainerstorage -y
```