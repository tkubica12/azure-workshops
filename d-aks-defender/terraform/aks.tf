resource "azurerm_kubernetes_cluster" "main" {
  name                      = "d-aks-defender"
  location                  = azurerm_resource_group.main.location
  resource_group_name       = azurerm_resource_group.main.name
  dns_prefix                = "d-aks-defender"
  azure_policy_enabled      = true

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_B2ms"
  }

  identity {
    type = "SystemAssigned"
  }

  microsoft_defender {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
  }
}
