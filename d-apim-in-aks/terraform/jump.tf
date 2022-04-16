// NIC
resource "azurerm_network_interface" "jump" {
  name                = "jump-nic"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.jump.id
    private_ip_address_allocation = "Dynamic"
  }
}

// Diagnostics storage account (for serial console access)
resource "azurerm_storage_account" "jump" {
  name                     = random_string.random.result
  resource_group_name      = azurerm_resource_group.demo.name
  location                 = azurerm_resource_group.demo.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

// VM
resource "azurerm_linux_virtual_machine" "jump" {
  name                            = "jumpvm"
  resource_group_name             = azurerm_resource_group.demo.name
  location                        = azurerm_resource_group.demo.location
  size                            = "Standard_B1ms"
  admin_username                  = "labuser"
  admin_password                  = "Azure12345678"
  disable_password_authentication = false

  network_interface_ids = [
    azurerm_network_interface.jump.id,
  ]

  boot_diagnostics {
    storage_account_uri = azurerm_storage_account.jump.primary_blob_endpoint
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}
