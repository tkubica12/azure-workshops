module "main_naming" {
  source = "Azure/naming/azurerm"
  suffix = ["sql"]
}

resource "azurerm_resource_group" "main" {
  name     = module.main_naming.resource_group.name_unique
  location = var.location
}
