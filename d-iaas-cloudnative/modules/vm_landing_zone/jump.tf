module "jump" {
  source = "Azure/naming/azurerm"
  suffix = [var.prefix, "jump"]
}


resource "azurerm_network_interface" "jump" {
  name                = module.jump.network_interface.name
  resource_group_name = var.resource_group_name
  location            = var.location

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_linux_virtual_machine" "jump" {
  name                            = module.jump.linux_virtual_machine.name
  resource_group_name             = var.resource_group_name
  location                        = var.location
  size                            = "Standard_B2s"
  admin_username                  = "tomas"
  admin_password                  = "Azure12345678"
  disable_password_authentication = false
  network_interface_ids           = [azurerm_network_interface.jump.id]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  boot_diagnostics {}
}
