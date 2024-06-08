resource "random_string" "main" {
  length  = 10
  special = false
  lower   = true
  upper   = false
  numeric = false
}

data "azurerm_client_config" "current" {}

