# Azure Kubernetes Service with API server VNET injection
Build the solution - Azure Firewall to filter outbound traffic with neccessary rules, network environment, routing, AKS.

```bash
az group create -n aksapivnet -l westus2
az bicep build -f main.bicep && az deployment group create -g aksapivnet --template-file main.json
```

Check Kubernetes does not have to use any tuneling now (no tunel-front or konnectivity pods):

```bash
az aks command invoke -n myaks -g aksapivnet -c "kubectl get pods -A"

NAMESPACE     NAME                                       READY   STATUS              RESTARTS   AGE
aks-command   command-b53865b7dd944e7b93ad5a9126b3df61   0/1     ContainerCreating   0          6s
kube-system   azure-cns-m2w25                            1/1     Running             0          4m43s
kube-system   azure-cns-xlf7c                            1/1     Running             0          4m33s
kube-system   cloud-node-manager-6ml4z                   1/1     Running             0          4m33s
kube-system   cloud-node-manager-6qlw8                   1/1     Running             0          4m43s
kube-system   coredns-autoscaler-7d56cd888-l7btx         1/1     Running             0          8m23s
kube-system   coredns-dc97c5f55-2qj2c                    1/1     Running             0          4m13s
kube-system   coredns-dc97c5f55-c5gbc                    1/1     Running             0          8m23s
kube-system   csi-azuredisk-node-hnb5g                   3/3     Running             0          4m33s
kube-system   csi-azuredisk-node-xzqc5                   3/3     Running             0          4m43s
kube-system   csi-azurefile-node-vrlqk                   3/3     Running             0          4m43s
kube-system   csi-azurefile-node-wh6ld                   3/3     Running             0          4m33s
kube-system   kube-proxy-kkbm5                           1/1     Running             0          4m33s
kube-system   kube-proxy-mz66j                           1/1     Running             0          4m43s
kube-system   metrics-server-64b66fbbc8-rwnm4            0/1     Running             0          8m22s
```