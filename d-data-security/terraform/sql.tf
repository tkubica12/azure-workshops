resource "azurerm_mssql_server" "main" {
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
  name           = "sql-db"
  server_id      = azurerm_mssql_server.main.id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  license_type   = "LicenseIncluded"
  max_size_gb    = 4
  read_scale     = false
  ledger_enabled = true
  zone_redundant = false
  sku_name       = "GP_DC_2"
}

resource "azurerm_key_vault_key" "tde" {
  name         = "key-tde"
  key_vault_id = azurerm_key_vault.main.id
  key_type     = "RSA"
  key_size     = 2048

  depends_on = [
    azurerm_key_vault_access_policy.main
  ]

  key_opts = [
    "unwrapKey",
    "wrapKey",
  ]
}

resource "azurerm_key_vault_access_policy" "tde" {
  key_vault_id = azurerm_key_vault.main.id
  tenant_id    = azurerm_mssql_server.main.identity.0.tenant_id
  object_id    = azurerm_mssql_server.main.identity.0.principal_id

  key_permissions = [
    "WrapKey",
    "UnwrapKey",
    "Get"
  ]
}

resource "azurerm_mssql_server_transparent_data_encryption" "main" {
  server_id        = azurerm_mssql_server.main.id
  key_vault_key_id = azurerm_key_vault_key.tde.id

  depends_on = [
    azurerm_key_vault_access_policy.tde,
    azurerm_key_vault_key.tde
  ]
}

resource "azurerm_attestation_provider" "main" {
  name                = random_string.main.result
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
}