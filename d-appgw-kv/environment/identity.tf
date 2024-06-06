resource "azurerm_user_assigned_identity" "jump" {
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  name                = "jump-identity"
}

resource "azurerm_role_assignment" "rg" {
  scope                = azurerm_resource_group.main.id
  role_definition_name = "Owner"
  principal_id         = azurerm_user_assigned_identity.jump.principal_id
}
