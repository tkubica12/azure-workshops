// AKS
resource "azurerm_kubernetes_cluster" "aks_remote_write" {
  name                = "d-prometheus-remotewrite"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "d-prometheus-remotewrite"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_B2ms"
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_role_assignment" "aks_remote_write" {
  role_definition_name = "Monitoring Metrics Publisher"
  scope                = jsondecode(azapi_resource.az_monitor_workspace.output).properties.defaultIngestionSettings.dataCollectionRuleResourceId
  principal_id         = azurerm_kubernetes_cluster.aks_remote_write.kubelet_identity[0].object_id
}
