resource "azurerm_postgresql_flexible_server" "psql_main" {
  count                        = var.psql_scenario ? 1 : 0
  name                         = module.naming_main.postgresql_server.name_unique
  resource_group_name          = azurerm_resource_group.main.name
  location                     = var.main_region
  version                      = "16"
  delegated_subnet_id          = azurerm_subnet.psql_subnet_main[0].id
  private_dns_zone_id          = azurerm_private_dns_zone.dns[0].id
  administrator_login          = "tomas"
  administrator_password       = random_string.password.result
  zone                         = "1"
  storage_mb                   = 32768
  storage_tier                 = "P4"
  sku_name                     = "GP_Standard_D2ds_v5"
  geo_redundant_backup_enabled = true
  depends_on                   = [azurerm_private_dns_zone_virtual_network_link.dns_main[0]]
}

resource "azurerm_postgresql_flexible_server" "psql_target" {
  count                        = var.psql_scenario && var.directreplication_scenario ? 1 : 0
  name                         = module.naming_target.postgresql_server.name_unique
  resource_group_name          = azurerm_resource_group.target.name
  location                     = var.main_region
  version                      = "16"
  delegated_subnet_id          = azurerm_subnet.psql_subnet_target[0].id
  private_dns_zone_id          = azurerm_private_dns_zone.dns[0].id
  administrator_login          = "tomas"
  administrator_password       = random_string.password.result
  zone                         = "1"
  storage_mb                   = 32768
  storage_tier                 = "P4"
  sku_name                     = "GP_Standard_D2ds_v5"
  geo_redundant_backup_enabled = false
  create_mode                  = "Replica"
  source_server_id             = azurerm_postgresql_flexible_server.psql_main[0].id

  depends_on = [
    azurerm_private_dns_zone_virtual_network_link.dns_target[0],
    azurerm_virtual_network_peering.main2target,
    azurerm_virtual_network_peering.target1main
  ]
}
