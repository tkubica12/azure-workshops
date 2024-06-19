resource "azurerm_resource_group" "main" {
  name     = module.base_naming.resource_group.name
  location = var.location
}

data "azurerm_client_config" "current" {}