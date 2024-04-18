resource "azurerm_mssql_server" "main" {
  name                         = module.main_naming.sql_server.name_unique
  resource_group_name          = azurerm_resource_group.main.name
  location                     = azurerm_resource_group.main.location
  version                      = "12.0"
  administrator_login          = "tomas"
  administrator_login_password = "Azure12345678"
}

resource "azurerm_mssql_database" "main" {
  name           = "exampledb"
  server_id      = azurerm_mssql_server.main.id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  license_type   = "LicenseIncluded"
  read_scale     = false
  sku_name       = "S0"
  zone_redundant = false
}

resource "azurerm_monitor_diagnostic_setting" "example" {
  name                           = azurerm_mssql_server.main.name
  target_resource_id             = azurerm_mssql_database.main.id
  eventhub_authorization_rule_id = azurerm_eventhub_namespace_authorization_rule.main.id
  eventhub_name                  = azurerm_eventhub.main.name

  enabled_log {
    category = "SQLSecurityAuditEvents"
  }

  metric {
    category = "AllMetrics"
  }

  lifecycle {
    ignore_changes = [enabled_log, metric]
  }
}

resource "azurerm_mssql_database_extended_auditing_policy" "main" {
  database_id                             = azurerm_mssql_database.main.id
  log_monitoring_enabled                  = true
  storage_endpoint                        = azurerm_storage_account.main.primary_blob_endpoint
  storage_account_access_key              = azurerm_storage_account.main.primary_access_key
  storage_account_access_key_is_secondary = false
  retention_in_days                       = 2
}
