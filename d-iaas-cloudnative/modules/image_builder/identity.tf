resource "azurerm_user_assigned_identity" "main" {
  name                = module.naming.user_assigned_identity.name
  location            = var.location
  resource_group_name = var.resource_group_name
}

resource "azurerm_role_assignment" "image_builder" {
  scope                = azurerm_resource_group.staging.id
  role_definition_name = "Contributor"
  principal_id         = azurerm_user_assigned_identity.main.principal_id
}

data "azurerm_resource_group" "images" {
  name = var.resource_group_name
}

resource "azurerm_role_assignment" "image_writer" {
  scope                = data.azurerm_resource_group.images.id
  role_definition_name = "Contributor"
  principal_id         = azurerm_user_assigned_identity.main.principal_id
}
