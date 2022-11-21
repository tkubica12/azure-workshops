resource "azurerm_private_dns_zone" "storage" {
  name                = "privatelink.blob.core.windows.net"
  resource_group_name = azurerm_resource_group.global.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "primary" {
  name                  = "primary"
  resource_group_name   = azurerm_resource_group.global.name
  private_dns_zone_name = azurerm_private_dns_zone.storage.name
  virtual_network_id    = module.network_primary.spoke1_id
}

resource "azurerm_private_dns_zone_virtual_network_link" "secondary" {
  name                  = "secondary"
  resource_group_name   = azurerm_resource_group.global.name
  private_dns_zone_name = azurerm_private_dns_zone.storage.name
  virtual_network_id    = module.network_secondary.spoke1_id
}
