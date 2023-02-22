resource "azurerm_resource_group" "main" {
  name     = "d-scalability"
  location = var.location
}

resource "random_string" "main" {
  length  = 12
  special = false
  upper   = false
  lower   = true
  numeric = false
}
