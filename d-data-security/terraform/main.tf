resource "azurerm_resource_group" "main" {
  name     = "d-data-and-compute-security"
  location = "West Europe"
}

data "azurerm_client_config" "current" {
}

resource "random_string" "main" {
  length  = 10
  lower   = true
  numeric = false
  upper   = false
  special = false
}

resource "random_string" "short" {
  length  = 4
  lower   = true
  numeric = false
  upper   = false
  special = false
}
