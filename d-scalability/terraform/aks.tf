resource "azurerm_kubernetes_cluster" "main" {
  count               = var.aks_count
  name                = "aks${count.index}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "aks${count.index}"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_B2s"
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azapi_resource" "flux_extension" {
  count     = var.aks_count
  type      = "Microsoft.KubernetesConfiguration/extensions@2021-09-01"
  name      = "flux"
  parent_id = azurerm_kubernetes_cluster.main[count.index].id

  identity {
    type = "SystemAssigned"
  }

  body = jsonencode({
    properties = {
      extensionType           = "microsoft.flux"
      autoUpgradeMinorVersion = true
    }
  })
}

resource "azapi_resource" "flux_config" {
  count                     = var.aks_count
  type                      = "Microsoft.KubernetesConfiguration/fluxConfigurations@2022-03-01"
  name                      = "myconfig"
  parent_id                 = azurerm_kubernetes_cluster.main[count.index].id
  schema_validation_enabled = false

  depends_on = [
    azapi_resource.flux_extension
  ]

  identity {
    type = "SystemAssigned"
  }

  body = jsonencode({
    properties = {
      scope      = "cluster"
      namespace  = "flux-system"
      sourceKind = "GitRepository"
      kustomizations = {
        myapp = {
          name                   = "myapp"
          path                   = "./myapp"
          force                  = true
          prune                  = true
          timeoutInSeconds       = 120
          intervalInSeconds      = 60
          retryIntervalInSeconds = 60
        }
      }
      gitRepository = {
        url                   = "https://github.com/tkubica12/myapp-flux"
        timeoutInSeconds      = 120
        syncIntervalInSeconds = 60
        repositoryRef = {
          branch = "main"
        }
      }
    }
  })
}
