resource "azurerm_resource_group" "main" {
  name     = "d-aks-kata"
  location = var.location
}
