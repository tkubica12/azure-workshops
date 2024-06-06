resource "azurerm_user_assigned_identity" "appgw" {
  resource_group_name = var.resource_group_name
  location            = var.location
  name                = "appgw-identity"
}

resource "azurerm_role_assignment" "kv_appgw" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_user_assigned_identity.appgw.principal_id
}
