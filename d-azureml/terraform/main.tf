variable "location" {
  type    = string
  default = "northeurope"
}

resource "azurerm_resource_group" "demo" {
  name     = "d-azurelm"
  location = var.location
}

data "azurerm_client_config" "current" {}

resource "random_string" "random" {
  length  = 8
  special = false
  numeric = true
  lower   = true
  upper   = false
}