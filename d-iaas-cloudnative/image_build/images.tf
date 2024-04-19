resource "azurerm_shared_image_gallery" "main" {
  name                = "myimages"
  resource_group_name = azurerm_resource_group.images.name
  location            = azurerm_resource_group.images.location
  description         = "My company images"
}

resource "azurerm_shared_image" "nginx" {
  name                = "my-nginx-image"
  gallery_name        = azurerm_shared_image_gallery.main.name
  resource_group_name = azurerm_resource_group.images.name
  location            = azurerm_resource_group.images.location
  os_type             = "Linux"
  hyper_v_generation  = "V2"

  identifier {
    publisher = "mycompany"
    offer     = "linux"
    sku       = "nginx"
  }
}
