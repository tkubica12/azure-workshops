resource "azurerm_mssql_server" "main" {
  count                        = var.enable_sql ? 1 : 0
  name                         = random_string.main.result
  resource_group_name          = azurerm_resource_group.main.name
  location                     = azurerm_resource_group.main.location
  version                      = "12.0"
  administrator_login          = "tomas"
  administrator_login_password = "Azure12345678"

  azuread_administrator {
    login_username = var.current_user_name
    object_id      = data.azurerm_client_config.current.object_id
    tenant_id      = data.azurerm_client_config.current.tenant_id
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_mssql_database" "main" {
  count          = var.enable_sql ? 1 : 0
  name           = "sql-db"
  server_id      = azurerm_mssql_server.main[0].id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  license_type   = "LicenseIncluded"
  max_size_gb    = 4
  read_scale     = false
  ledger_enabled = true
  zone_redundant = false
  sku_name       = "GP_DC_2"
}

resource "azurerm_key_vault_key" "tde" {
  count        = var.enable_sql ? 1 : 0
  name         = "key-tde"
  key_vault_id = azurerm_key_vault.main.id
  key_type     = "RSA"
  key_size     = 2048

  depends_on = [
    azurerm_role_assignment.kv_main
  ]

  key_opts = [
    "unwrapKey",
    "wrapKey",
  ]
}

resource "azurerm_role_assignment" "kv_tde" {
  count                = var.enable_sql ? 1 : 0
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Crypto Service Encryption User"
  principal_id         = azurerm_mssql_server.main[0].identity.0.principal_id
}

resource "azurerm_mssql_server_transparent_data_encryption" "main" {
  count            = var.enable_sql ? 1 : 0
  server_id        = azurerm_mssql_server.main[0].id
  key_vault_key_id = azurerm_key_vault_key.tde[0].id

  depends_on = [
    azurerm_role_assignment.kv_tde,
    azurerm_key_vault_key.tde
  ]
}

resource "azurerm_attestation_provider" "main" {
  count               = var.enable_sql ? 1 : 0
  name                = random_string.main.result
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
}
