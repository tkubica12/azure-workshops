
resource "azurerm_network_interface" "vm3" {
  name                = "win-vm3"
  location            = var.primary_location
  resource_group_name = azurerm_resource_group.zrs.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = module.network_primary.spoke1_subnet1_id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_windows_virtual_machine" "vm3" {
  name                = "win-vm3"
  location            = var.primary_location
  resource_group_name = azurerm_resource_group.zrs.name
  size                = "Standard_B2ms"
  admin_username      = "tomas"
  admin_password      = "Azure12345678"
  zone                = 1

  network_interface_ids = [
    azurerm_network_interface.zrs.id,
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Premium_ZRS"
  }

  source_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2022-Datacenter"
    version   = "latest"
  }

  depends_on = [
    module.network_primary
  ]
}
