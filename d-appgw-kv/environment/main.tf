resource "azurerm_resource_group" "main" {
  name     = "rg-appgw-kv-cert"
  location = "swedencentral"
}

resource "random_string" "main" {
  length  = 10
  special = false
  lower   = true
  upper   = false
  numeric = false
}

data "azurerm_client_config" "current" {}

