// Resource Group
resource "azurerm_resource_group" "main" {
  name     = "d-storage-blob"
  location = var.location
}

// Random suffix
resource "random_string" "storage" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

// Get current account data
data "azurerm_client_config" "current" {}