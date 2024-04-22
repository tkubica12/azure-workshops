module "naming" {
  source = "Azure/naming/azurerm"
  suffix = var.prefixes
}

data "azurerm_client_config" "current" {}
