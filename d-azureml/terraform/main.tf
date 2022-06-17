variable "location" {
  type    = string
  default = "northeurope"
}

resource "azurerm_resource_group" "demo" {
  name     = "d-azurelm"
  location = var.location
}

data "azurerm_client_config" "current" {}
