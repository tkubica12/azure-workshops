resource "azurerm_user_assigned_identity" "workshop" {
  name                = "workshop-identity"
  resource_group_name = azurerm_resource_group.workshop.name
  location            = azurerm_resource_group.workshop.location
}
