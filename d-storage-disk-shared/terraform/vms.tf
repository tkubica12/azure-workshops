// NIC1
resource "azurerm_network_interface" "vm1" {
  name                = "vm1-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Static"
    private_ip_address            = "10.0.0.10"
  }
}

// VM1
resource "azurerm_linux_virtual_machine" "vm1" {
  name                            = "vm1"
  location                        = azurerm_resource_group.main.location
  resource_group_name             = azurerm_resource_group.main.name
  network_interface_ids           = [azurerm_network_interface.vm1.id]
  size                            = "Standard_D2as_v4"
  computer_name                   = "vm1"
  admin_username                  = "tomas"
  disable_password_authentication = false
  admin_password                  = var.password

  os_disk {
    name                 = "vm1-osdisk"
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  boot_diagnostics {}
}
