resource "azurerm_kubernetes_cluster" "main" {
  name                = "d-aks-istio"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "d-aks-istio"

  monitor_metrics {}

  oms_agent {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
  }

  service_mesh_profile {
    mode                             = "Istio"
    external_ingress_gateway_enabled = true
  }

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_B4ms"
  }

  identity {
    type = "SystemAssigned"
  }
}
