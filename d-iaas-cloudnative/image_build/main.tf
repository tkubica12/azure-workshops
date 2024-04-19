resource "azurerm_resource_group" "images" {
  name     = "rg-images"
  location = var.location
}

resource "azurerm_resource_group" "staging" {
  name     = "rg-staging"
  location = var.location
}
