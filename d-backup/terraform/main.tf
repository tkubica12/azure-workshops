// Resource Group
resource "azurerm_resource_group" "main" {
  name     = "d-backup"
  location = var.location
}

// Random suffix
resource "random_string" "main" {
  length  = 12
  special = false
  upper   = false
  numeric = true
}

// Get current account data
data "azurerm_client_config" "current" {}