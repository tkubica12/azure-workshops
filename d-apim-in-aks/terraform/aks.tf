// AKS
resource "azurerm_kubernetes_cluster" "demo" {
  name                = "apim-demo-aks"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  dns_prefix          = "apim-demo-aks"

  default_node_pool {
    name           = "default"
    node_count     = 1
    vm_size        = "Standard_B2ms"
    vnet_subnet_id = azurerm_subnet.aks.id
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin     = "azure"
    service_cidr       = "192.168.0.0/20"
    dns_service_ip     = "192.168.0.10"
    docker_bridge_cidr = "172.16.0.0/22"
    outbound_type      = "userDefinedRouting"
  }

  depends_on = [
    azurerm_firewall.demo,
    azurerm_firewall_policy_rule_collection_group.common,
    azurerm_subnet_route_table_association.jump,
  ]
}

// RBAC - grant access to VNET
resource "azurerm_role_assignment" "demo" {
  scope                = azurerm_virtual_network.demo.id
  role_definition_name = "Network Contributor"
  principal_id         = azurerm_kubernetes_cluster.demo.identity.0.principal_id
}