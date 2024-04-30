resource "azurerm_user_assigned_identity" "main" {
  name                = module.naming.user_assigned_identity.name
  resource_group_name = var.resource_group_name
  location            = var.location
}

resource "azurerm_role_assignment" "kv_self" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_role_assignment" "kv_umi" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_user_assigned_identity.main.principal_id
}

resource "azurerm_role_assignment" "kv_umi_reader" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Reader"
  principal_id         = azurerm_user_assigned_identity.main.principal_id
}
