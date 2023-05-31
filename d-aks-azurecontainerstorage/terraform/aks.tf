resource "azurerm_kubernetes_cluster" "main" {
  name                 = "d-aks-azurecontainerstorage"
  location             = azurerm_resource_group.main.location
  resource_group_name  = azurerm_resource_group.main.name
  dns_prefix           = "d-aks-azurecontainerstorage"
  azure_policy_enabled = false
  kubernetes_version   = "1.25"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_B4ms"

    node_labels = {
      "acstor.azure.com/io-engine" = "acstor"
    }

    # linux_os_config {
    #   transparent_huge_page_enabled = "always"
    #   transparent_huge_page_defrag  = "always"
    # }
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_kubernetes_cluster_extension" "acstor" {
  name              = "acstor"
  cluster_id        = azurerm_kubernetes_cluster.main.id
  extension_type    = "microsoft.azurecontainerstorage"
  release_train     = "prod"
  release_namespace = "acstor"

  depends_on = [ azurerm_role_assignment.mcrgcontributor ]
}

# resource "azapi_resource" "acstor" {
#   type      = "Microsoft.KubernetesConfiguration/extensions@2022-11-01"
#   name      = "acstor"
#   parent_id = azurerm_kubernetes_cluster.main.id

#   identity {
#     type = "SystemAssigned"
#   }

#   body = jsonencode({
#     properties = {
#       autoUpgradeMinorVersion        = true
#       configurationProtectedSettings = {}
#       configurationSettings          = {}
#       extensionType                  = "microsoft.azurecontainerstorage"
#       releaseTrain                   = "prod"
#       scope = {
#         cluster = {
#           releaseNamespace = "acstor"
#         }
#       }
#     }
#   })
# }

# resource "azurerm_user_assigned_identity" "main" {
#   name                = "identity"
#   location            = azurerm_resource_group.main.location
#   resource_group_name = azurerm_resource_group.main.name
# }

# resource "azurerm_role_assignment" "identityoperator" {
#   scope                = azurerm_user_assigned_identity.main.id
#   role_definition_name = "Managed Identity Operator"
#   principal_id         = azurerm_user_assigned_identity.main.principal_id
# }

data "azurerm_resource_group" "rgcontributor" {
  name = azurerm_kubernetes_cluster.main.node_resource_group
}

resource "azurerm_role_assignment" "rgcontributor" {
  scope                = azurerm_resource_group.main.id
  role_definition_name = "Contributor"
  principal_id         = azurerm_kubernetes_cluster.main.kubelet_identity[0].object_id
}

resource "azurerm_role_assignment" "mcrgcontributor" {
  scope                = data.azurerm_resource_group.rgcontributor.id
  role_definition_name = "Contributor"
  principal_id         = azurerm_kubernetes_cluster.main.kubelet_identity[0].object_id
}
