variable "location" {
  type    = string
  default = "northeurope"
}

# Resource Group
resource "azurerm_resource_group" "demo" {
  name     = "apim-demo-aks"
  location = var.location
}
