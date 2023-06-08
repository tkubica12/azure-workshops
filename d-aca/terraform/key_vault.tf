resource "azurerm_key_vault" "main" {
  name                       = random_string.main.result
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  soft_delete_retention_days = 7
  enable_rbac_authorization  = true
}

resource "azurerm_role_assignment" "kv_current" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Administrator"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_user_assigned_identity" "kv_reader" {
  name                = "kv_reader"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_role_assignment" "kv_reader" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Administrator"
  principal_id         = azurerm_user_assigned_identity.kv_reader.principal_id
}

resource "azurerm_key_vault_secret" "main" {
  name         = "mysecret"
  value        = "this_is_confidential!"
  key_vault_id = azurerm_key_vault.main.id

  depends_on = [
    azurerm_role_assignment.kv_current,
    time_sleep.wait_60_seconds
  ]
}

resource "time_sleep" "wait_60_seconds" {
  create_duration = "60s"

  depends_on = [azurerm_role_assignment.kv_reader]
}
