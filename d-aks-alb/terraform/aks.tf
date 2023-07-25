resource "azurerm_kubernetes_cluster" "main" {
  name                      = "d-aks-alb"
  location                  = azurerm_resource_group.main.location
  resource_group_name       = azurerm_resource_group.main.name
  dns_prefix                = "d-aks-alb"
  azure_policy_enabled      = true
  oidc_issuer_enabled       = true
  workload_identity_enabled = true

  default_node_pool {
    name                        = "default"
    node_count                  = 2
    enable_auto_scaling         = true
    min_count                   = 2
    max_count                   = 5
    vm_size                     = "Standard_B2ms"
    temporary_name_for_rotation = "defaulttemp"
    vnet_subnet_id              = azurerm_subnet.main.id
  }

  network_profile {
    network_plugin = "azure"
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

