module "base_naming" {
  source = "Azure/naming/azurerm"
  suffix = [var.prefix]
}

locals {
  dev_center                    = "${var.prefix}-devcenter"
  dev_project                   = "${var.prefix}-devproject"
  dev_center_managed_network_rg = "${module.base_naming.resource_group.name}-managed"
}
