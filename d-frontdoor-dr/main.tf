resource "azurerm_resource_group" "main" {
  name     = "rg-fd-dr-demo"
  location = var.app_location
}

resource "random_string" "main" {
  length  = 8
  special = false
  lower   = true
  upper   = false
  numeric = false
}
