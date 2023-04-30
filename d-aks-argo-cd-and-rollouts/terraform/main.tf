resource "azurerm_resource_group" "main" {
  name     = "d-aks-argo-cd-and-rollouts"
  location = "swedencentral"
}

resource "random_string" "main" {
  length  = 16
  lower   = true
  upper   = false
  special = false
  numeric = false
}