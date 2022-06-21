resource "azurerm_user_assigned_identity" "aks" {
  resource_group_name = azurerm_resource_group.demo.name
  location            = azurerm_resource_group.demo.location
  name = "aks"
}

resource "azurerm_user_assigned_identity" "aml" {
  resource_group_name = azurerm_resource_group.demo.name
  location            = azurerm_resource_group.demo.location
  name = "aml"
}

resource "azurerm_role_assignment" "aks" {
  scope                = azurerm_resource_group.demo.id
  role_definition_name = "Contributor"
  principal_id         = azurerm_user_assigned_identity.aks.principal_id
}

resource "azurerm_role_assignment" "aml" {
  scope                = azurerm_resource_group.demo.id
  role_definition_name = "Contributor"
  principal_id         = azurerm_user_assigned_identity.aml.principal_id
}