resource "azurerm_user_assigned_identity" "psql" {
  name                = "psql-identity${local.base_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}