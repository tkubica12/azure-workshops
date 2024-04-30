module "naming" {
  source = "Azure/naming/azurerm"
  suffix = [var.prefix, "ib"]
}

resource "azurerm_resource_group" "staging" {
  name     = "${module.naming.resource_group.name}-staging"
  location = var.location
}
