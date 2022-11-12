resource "azurerm_kubernetes_cluster" "reg1" {
  name                = "aks-${local.reg1}"
  location            = local.reg1
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "aks-${local.reg1}"

  network_profile {
    network_plugin     = "azure"
    load_balancer_sku  = "standard"
    outbound_type      = "loadBalancer"
    docker_bridge_cidr = "172.16.0.0/16"
    service_cidr       = "192.168.0.0/16"
    dns_service_ip     = "192.168.0.10"
  }

  default_node_pool {
    name            = "default"
    node_count      = 1
    vm_size         = "Standard_B2ms"
    os_disk_size_gb = 30
    vnet_subnet_id  = azurerm_subnet.reg1.id
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_kubernetes_cluster" "reg2" {
  name                = "aks-${local.reg2}"
  location            = local.reg2
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "aks-${local.reg2}"

  network_profile {
    network_plugin     = "azure"
    load_balancer_sku  = "standard"
    outbound_type      = "loadBalancer"
    docker_bridge_cidr = "172.16.0.0/16"
    service_cidr       = "192.168.0.0/16"
    dns_service_ip     = "192.168.0.10"
  }

  default_node_pool {
    name            = "default"
    node_count      = 1
    vm_size         = "Standard_B2ms"
    os_disk_size_gb = 30
    vnet_subnet_id  = azurerm_subnet.reg2.id
  }

  identity {
    type = "SystemAssigned"
  }
}
