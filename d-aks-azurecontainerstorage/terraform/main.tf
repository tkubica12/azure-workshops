resource "azurerm_resource_group" "main" {
  name     = "d-aks-azurecontainerstorage"
  location = "westeurope"
}

resource "random_string" "main" {
  length  = 16
  lower   = true
  upper   = false
  special = false
  numeric = false
}