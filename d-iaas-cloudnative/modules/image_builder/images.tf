resource "azurerm_shared_image_gallery" "main" {
  name                = module.naming.shared_image_gallery.name
  resource_group_name = var.resource_group_name
  location            = var.location
  description         = "My company images"
}

resource "azurerm_shared_image" "nginx" {
  name                = "${module.naming.shared_image.name}-nginx"
  gallery_name        = azurerm_shared_image_gallery.main.name
  resource_group_name = var.resource_group_name
  location            = var.location
  os_type             = "Linux"
  hyper_v_generation  = "V2"

  identifier {
    publisher = "mycompany"
    offer     = "linux"
    sku       = "nginx"
  }
}
