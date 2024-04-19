resource "azurerm_user_assigned_identity" "main" {
  name                = "uami-imagebuilder"
  location            = azurerm_resource_group.images.location
  resource_group_name = azurerm_resource_group.images.name
}

resource "azurerm_role_assignment" "image_builder" {
  scope                = azurerm_resource_group.staging.id
  role_definition_name = "Contributor"
  principal_id         = azurerm_user_assigned_identity.main.principal_id
}

resource "azurerm_role_assignment" "image_writer" {
  scope                = azurerm_resource_group.images.id
  role_definition_name = "Contributor"
  principal_id         = azurerm_user_assigned_identity.main.principal_id
}
