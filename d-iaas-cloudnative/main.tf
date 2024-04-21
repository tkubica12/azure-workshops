module "naming" {
  source = "Azure/naming/azurerm"
  suffix = [var.main_prefix]
}

resource "azurerm_resource_group" "images" {
  name     = "${module.naming.resource_group.name}-images"
  location = var.location
}

resource "azurerm_resource_group" "lz" {
  name     = "${module.naming.resource_group.name}-lz"
  location = var.location
}

resource "azurerm_resource_group" "vms" {
  name     = "${module.naming.resource_group.name}-vms"
  location = var.location
}

// Image Builder
module "image_builder" {
  source              = "./modules/image_builder"
  location            = var.location
  resource_group_name = azurerm_resource_group.images.name
  prefix              = var.main_prefix
}

// Landing Zone
module "vm_landing_zone" {
  source              = "./modules/vm_landing_zone"
  location            = var.location
  resource_group_name = azurerm_resource_group.lz.name
  prefix              = var.main_prefix
}

// Demo NGINX
module "demo_nginx" {
  source              = "./modules/vm_nginx"
  location            = var.location
  resource_group_name = azurerm_resource_group.vms.name
  prefix              = var.main_prefix
  vm_size             = "Standard_B1s"
  image_id            = module.image_builder.nginx_image_id
  subnet_id           = module.vm_landing_zone.subnet_id

  depends_on = [
    module.vm_landing_zone
  ]
}
