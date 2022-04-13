# AKS
resource "azurerm_kubernetes_cluster" "demo" {
  name                = "operators-demo-aks"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  dns_prefix          = "operators-demo-aks"

  default_node_pool {
    name       = "default"
    node_count = 5
    vm_size    = "Standard_B4ms"
  }

  identity {
    type = "SystemAssigned"
  }
}

# AKS GitOps operator (Flux v2)
resource "azapi_resource" "fluxextension" {
  type      = "Microsoft.KubernetesConfiguration/extensions@2022-03-01"
  name      = "flux"
  parent_id = azurerm_kubernetes_cluster.demo.id

  body = jsonencode({
    properties = {
      extensionType           = "microsoft.flux"
      autoUpgradeMinorVersion = true
    }
  })

}

resource "azapi_resource" "flux" {
  type      = "Microsoft.KubernetesConfiguration/fluxConfigurations@2022-03-01"
  name      = "/operators-demo-aks"
  parent_id = azurerm_kubernetes_cluster.demo.id

  depends_on = [
    azapi_resource.fluxextension
  ]

  body = jsonencode({
    properties = {
      scope      = "cluster"
      namespace  = "gitops-demo"
      sourceKind = "GitRepository"
      suspend    = false
      gitRepository = {
        url : "https://github.com/tkubica12/azure-workshops/"
        syncIntervalInSeconds : 30
        repositoryRef = {
          branch = "main"
        }
      }
      kustomizations = {
        platform = {
          path                   = "./d-kubernetes-operators/platform"
          syncIntervalInSeconds  = 120
          retryIntervalInSeconds = 120
          prune                  = true
          force                  = true
        }
        demo = {
          path                   = "./d-kubernetes-operators/demo"
          syncIntervalInSeconds  = 30
          retryIntervalInSeconds = 30
          prune                  = true
          force                  = true
        }
      }
    }
  })

}


#  Request body:
# cli.azure.cli.core.sdk.policies: {"properties": {"extensionType": "microsoft.flux", "autoUpgradeMinorVersion": true}}
# urllib3.connectionpool: https://management.azure.com:443 "PUT /subscriptions/a0f4a733-4fce-4d49-b8a8-d30541fc1b45/resourceGroups/operators-demo-aks/providers/Microsoft.ContainerService/managedClusters/operators-demo-aks/providers/Microsoft.KubernetesConfiguration/extensions/flux?api-version=2022-03-01 HTTP/1.1" 201 827


# Request body:
# cli.azure.cli.core.sdk.policies: {"properties": {"scope": "cluster", "namespace": "gitops-demo", "sourceKind": "GitRepository", "suspend": false, "gitRepository": {"url": "https://github.com/tkubica12/azure-workshops/", "syncIntervalInSeconds": 30, "repositoryRef": {"branch": "main"}}, "kustomizations": {"platform": {"path": "./d-kubernetes-operators/platform", "syncIntervalInSeconds": 120, "retryIntervalInSeconds": 120, "prune": true, "force": true}, "demo": {"path": "./d-kubernetes-operators/demo", "syncIntervalInSeconds": 30, "retryIntervalInSeconds": 30, "prune": true, "force": true}}}}
# urllib3.connectionpool: Starting new HTTPS connection (1): management.azure.com:443
# urllib3.connectionpool: https://management.azure.com:443 "PUT /subscriptions/a0f4a733-4fce-4d49-b8a8-d30541fc1b45/resourceGroups/operators-demo-aks/providers/Microsoft.ContainerService/managedClusters/operators-demo-aks/providers/Microsoft.KubernetesConfiguration/fluxConfigurations/operators-demo-aks?api-version=2022-03-01 HTTP/1.1" 201 1554
