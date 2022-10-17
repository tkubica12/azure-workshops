resource "azurerm_resource_group" "networking" {
  name     = "d-aks-cni-overlay-networking"
  location = "westcentralus"
}

resource "azurerm_resource_group" "aks" {
  name     = "d-aks-cni-overlay-aks"
  location = "westcentralus"
}