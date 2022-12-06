data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "main" {
  name                       = random_string.main.result
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  enable_rbac_authorization  = true
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days = 7
  purge_protection_enabled   = false
  sku_name                   = "standard"
}

resource "azurerm_role_assignment" "kv_admin" {
  role_definition_name = "Key Vault Administrator"
  scope                = azurerm_key_vault.main.id
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_role_assignment" "kv_access" {
  role_definition_name = "Key Vault Secrets User"
  scope                = azurerm_key_vault.main.id
  principal_id         = azurerm_user_assigned_identity.kv_access.principal_id
}

resource "azurerm_key_vault_secret" "main" {
  name         = "mysecret"
  value        = "ThisIsVerySecret!"
  key_vault_id = azurerm_key_vault.main.id

  depends_on = [
    azurerm_role_assignment.kv_admin
  ]
}