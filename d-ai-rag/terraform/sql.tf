resource "random_password" "sql" {
  length  = 16
  special = true
}

resource "azurerm_mssql_server" "main" {
  name                         = "sql-${local.base_name}"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = azurerm_resource_group.main.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = random_password.sql.result
}

resource "azurerm_mssql_database" "main" {
  name                        = "demo"
  server_id                   = azurerm_mssql_server.main.id
  max_size_gb                 = 32
  sku_name                    = "GP_S_Gen5_6"
  auto_pause_delay_in_minutes = 60
  geo_backup_enabled          = false
  min_capacity                = 1
}

resource "azurerm_mssql_firewall_rule" "main" {
  name             = "allow-all-fw"
  server_id        = azurerm_mssql_server.main.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "255.255.255.255"
}

output "SQL_PASSWORD" {
  value     = random_password.sql.result
  sensitive = true
}

output "SQL_SERVER_FQDN" {
  value = azurerm_mssql_server.main.fully_qualified_domain_name
}

output "SQL_USERNAME" {
  value = azurerm_mssql_server.main.administrator_login
}

output "SQL_DATABASE" {
  value = azurerm_mssql_database.main.name
}