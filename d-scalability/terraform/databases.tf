# resource "azurerm_mssql_server" "main" {
#   name                         = random_string.main.result
#   resource_group_name          = azurerm_resource_group.main.name
#   location                     = azurerm_resource_group.main.location
#   version                      = "12.0"
#   administrator_login          = "tomas"
#   administrator_login_password = "Azure12345678"
# }

# resource "azurerm_mssql_database" "db" {
#   name           = "sql-db"
#   server_id      = azurerm_mssql_server.main.id
#   collation      = "SQL_Latin1_General_CP1_CI_AS"
#   license_type   = "LicenseIncluded"
#   max_size_gb    = 4
#   read_scale     = true
#   sku_name       = "BC_Gen5_2"
#   zone_redundant = true
# }

# resource "azurerm_mssql_database" "hyperscale" {
#   name           = "sql-hyperscale"
#   server_id      = azurerm_mssql_server.main.id
#   collation      = "SQL_Latin1_General_CP1_CI_AS"
#   license_type   = "LicenseIncluded"
#   read_scale     = false
#   sku_name       = "HS_Gen5_2"
#   zone_redundant = false
# }

# resource "azurerm_cosmosdb_account" "main" {
#   name                = random_string.main.result
#   location            = azurerm_resource_group.main.location
#   resource_group_name = azurerm_resource_group.main.name
#   offer_type          = "Standard"
#   kind                = "GlobalDocumentDB"

#   geo_location {
#     location          = azurerm_resource_group.main.location
#     failover_priority = 0
#   }

#   consistency_policy {
#     consistency_level       = "Session"
#     max_interval_in_seconds = 5
#     max_staleness_prefix    = 100
#   }
# }

# resource "azurerm_cosmosdb_sql_database" "main" {
#   name                = "cosmos-db"
#   resource_group_name = azurerm_resource_group.main.name
#   account_name        = azurerm_cosmosdb_account.main.name
# }

# resource "azurerm_cosmosdb_sql_container" "main" {
#   name                  = "cosmos-collection"
#   resource_group_name   = azurerm_resource_group.main.name
#   account_name          = azurerm_cosmosdb_account.main.name
#   database_name         = azurerm_cosmosdb_sql_database.main.name
#   throughput            = 400
#   partition_key_path    = "/definition/id"
#   partition_key_version = 1
# }
