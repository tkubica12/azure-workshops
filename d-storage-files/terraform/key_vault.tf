resource "azurerm_key_vault" "main" {
  name                       = random_string.storage.result
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  enable_rbac_authorization  = true
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days = 7
  purge_protection_enabled   = false
  sku_name                   = "standard"
}

resource "azurerm_role_assignment" "kv" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Administrator"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_key_vault_secret" "password" {
  name         = "password"
  value        = random_password.users.result
  key_vault_id = azurerm_key_vault.main.id

  depends_on = [
    azurerm_role_assignment.kv
  ]
}