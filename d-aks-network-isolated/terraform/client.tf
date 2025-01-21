
resource "azurerm_windows_virtual_machine" "client_vm" {
  name                  = "${local.base_name}-client-vm"
  location              = azurerm_resource_group.main.location
  resource_group_name   = azurerm_resource_group.main.name
  network_interface_ids = [azurerm_network_interface.client_vm.id]
  size                  = "Standard_B4ms"
  computer_name         = "client-vm"

  os_disk {
    name                 = "${local.base_name}-osdisk"
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "MicrosoftWindowsDesktop"
    offer     = "Windows-11"
    sku       = "win11-24h2-pron"
    version   = "latest"
  }

  admin_username = "adminuser"
  admin_password = "Azure12345678"
}

resource "azurerm_network_interface" "client_vm" {
  name                = "${local.base_name}-client-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.client.id
    private_ip_address_allocation = "Dynamic"
  }
}
