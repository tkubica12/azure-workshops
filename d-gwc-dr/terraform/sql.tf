# Azure SQL in main region
resource "azurerm_mssql_server" "sql_main" {
  count                        = (var.directreplication_scenario || var.indirectreplication_scenario) && var.sql_scenario ? 1 : 0
  name                         = module.naming_main.mssql_server.name_unique
  resource_group_name          = azurerm_resource_group.main.name
  location                     = var.main_region
  version                      = "12.0"
  administrator_login          = "tomas"
  administrator_login_password = random_string.password.result
}

resource "azurerm_mssql_database" "sql_main" {
  count          = (var.directreplication_scenario || var.indirectreplication_scenario) && var.sql_scenario ? 1 : 0
  name           = "db-drdemo"
  server_id      = azurerm_mssql_server.sql_main[0].id
  sku_name       = "GP_Gen5_2"
  zone_redundant = true
}


# Azure SQL replica in target region
module "sql_target" {
  source = "Azure/naming/azurerm"
  suffix = [local.target_region_short, "drdemo"]
}

resource "azurerm_mssql_server" "sql_target" {
  count                        = var.directreplication_scenario && var.sql_scenario ? 1 : 0
  name                         = module.naming_target.mssql_server.name_unique
  resource_group_name          = azurerm_resource_group.target.name
  location                     = var.target_region
  version                      = "12.0"
  administrator_login          = "tomas"
  administrator_login_password = random_string.password.result
}

# Azure SQL replication
resource "azurerm_mssql_failover_group" "replication" {
  count     = var.directreplication_scenario && var.sql_scenario ? 1 : 0
  name      = "${azurerm_mssql_server.sql_main[0].name}-fg"
  server_id = azurerm_mssql_server.sql_main[0].id

  databases = [
    azurerm_mssql_database.sql_main[0].id
  ]

  partner_server {
    id = azurerm_mssql_server.sql_target[0].id
  }

  read_write_endpoint_failover_policy {
    mode = "Manual"
  }
}
