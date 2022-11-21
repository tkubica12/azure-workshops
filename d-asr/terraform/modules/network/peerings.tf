resource "azurerm_virtual_network_peering" "peer_hub_spoke1" {
  name                         = "peer-hub-spoke1"
  resource_group_name          = var.rg_name
  virtual_network_name         = azurerm_virtual_network.hub.name
  remote_virtual_network_id    = azurerm_virtual_network.spoke1.id
  allow_virtual_network_access = true
  use_remote_gateways          = false
  allow_forwarded_traffic      = true
  allow_gateway_transit        = false
}

resource "azurerm_virtual_network_peering" "peer_spoke1_hub" {
  name                         = "peer-spoke1-hub"
  resource_group_name          = var.rg_name
  virtual_network_name         = azurerm_virtual_network.spoke1.name
  remote_virtual_network_id    = azurerm_virtual_network.hub.id
  allow_virtual_network_access = true
  use_remote_gateways          = false
  allow_forwarded_traffic      = true
  allow_gateway_transit        = false
}
