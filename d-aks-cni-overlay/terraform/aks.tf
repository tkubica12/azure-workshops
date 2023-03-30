resource "azurerm_kubernetes_cluster" "main" {
  name                = "d-aks-cni-overlay"
  location            = azurerm_resource_group.aks.location
  resource_group_name = azurerm_resource_group.aks.name
  dns_prefix          = "d-aks-cni-overlay"


  network_profile {
    network_policy      = "calico"
    network_plugin      = "azure"
    network_plugin_mode = "Overlay"
    service_cidr        = "192.168.196.0/22"
    dns_service_ip      = "192.168.196.10"
    outbound_type       = "userDefinedRouting"
  }

  default_node_pool {
    name                   = "system"
    node_count             = 2
    vm_size                = "Standard_B2ms"
    vnet_subnet_id         = azurerm_subnet.aks.id
    zones                  = [1, 2, 3]

    node_labels = {
      "dedication" = "system"
    }
  }

  identity {
    type         = "SystemAssigned"
  }

  depends_on = [
    azurerm_firewall.main,
    azurerm_subnet_route_table_association.main
  ]
}
