resource "azurerm_kubernetes_cluster" "aks1" {
  name                = "d-aks-argo-cd-and-rollouts"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "d-aks-argo-cd-and-rollouts"

  default_node_pool {
    name                        = "default"
    node_count                  = 1
    vm_size                     = "Standard_B4ms"
    temporary_name_for_rotation = "defaulttemp"
  }

  identity {
    type = "SystemAssigned"
  }

  lifecycle {
    ignore_changes = [
      azure_policy_enabled,
      microsoft_defender
    ]
  }
}
