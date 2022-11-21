// Global
resource "azurerm_resource_group" "global" {
  name     = "d-asr-global"
  location = var.primary_location
}

// Primary location
resource "azurerm_resource_group" "primary" {
  name     = "d-asr-primary"
  location = var.primary_location
}

module "network_primary" {
  source   = "./modules/network"
  name     = "primary"
  rg_name  = azurerm_resource_group.primary.name
  location = var.primary_location
  ip_range = "10.1.0.0/16"
}

// Secondary location
resource "azurerm_resource_group" "secondary" {
  name     = "d-asr-secondary"
  location = var.secondary_location
}

module "network_secondary" {
  source   = "./modules/network"
  name     = "secondary"
  rg_name  = azurerm_resource_group.secondary.name
  location = var.secondary_location
  ip_range = "10.1.0.0/16"
}

// Random string
resource "random_string" "main" {
  length  = 12
  upper   = false
  lower   = true
  numeric = false
  special = false
}


