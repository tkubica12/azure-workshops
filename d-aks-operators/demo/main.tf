variable "location" {
  type    = string
  default = "northeurope"
}

variable "password" {
  type    = string
  default = "Azure12345678"
}

variable "AZURE_SUBSCRIPTION_ID" {
  type    = string
}

variable "AZURE_TENANT_ID" {
  type    = string
}

variable "AZURE_CLIENT_ID" {
  type    = string
}

variable "AZURE_CLIENT_SECRET" {
  type    = string
}

# Resource Group
resource "azurerm_resource_group" "demo" {
  name     = "operators-demo-aks"
  location = var.location
}
