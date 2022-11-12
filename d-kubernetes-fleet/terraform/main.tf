locals {
  reg1 = "westeurope"
  reg2 = "eastus"
}

resource "azurerm_resource_group" "main" {
  name     = "d-kubernetes-fleet"
  location = "westeurope"
}