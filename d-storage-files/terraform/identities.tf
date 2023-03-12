resource "azurerm_user_assigned_identity" "identity1" {
  name                = "identity1"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_user_assigned_identity" "identity2" {
  name                = "identity2"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}