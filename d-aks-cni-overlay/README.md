# AKS with Azure CNI overlay mode to replace Kubenet


Register feature

```bash
az feature register --namespace Microsoft.ContainerService --name AzureOverlayPreview
az feature register --namespace Microsoft.Network --name AzureFirewallBasic
```