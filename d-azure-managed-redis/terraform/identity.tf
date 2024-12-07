resource "azurerm_user_assigned_identity" "app" {
  name                = "identity-${local.base_name}"
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
}
