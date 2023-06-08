resource "azurerm_resource_group" "main" {
  name     = "d-aca"
  location = "westeurope"
}

resource "random_string" "main" {
  length  = 16
  lower   = true
  upper   = false
  special = false
  numeric = false
}

data "azurerm_client_config" "current" {}