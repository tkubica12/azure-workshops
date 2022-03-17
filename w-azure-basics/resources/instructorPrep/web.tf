resource "azurerm_network_interface" "web" {
  name                = "web-nic"
  location            = azurerm_resource_group.workshop.location
  resource_group_name = azurerm_resource_group.workshop.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.sharedVnetSubnet.id
    private_ip_address_allocation = "Static"
    private_ip_address            = "10.254.0.100"
  }
}

resource "azurerm_storage_account" "web" {
  name                     = "tomaskubicastore58883542"
  resource_group_name      = azurerm_resource_group.workshop.name
  location                 = azurerm_resource_group.workshop.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_linux_virtual_machine" "web" {
  name                            = "web-vm"
  resource_group_name             = azurerm_resource_group.workshop.name
  location                        = azurerm_resource_group.workshop.location
  size                            = "Standard_B1ms"
  admin_username                  = "tomas"
  admin_password                  = var.password
  disable_password_authentication = false
  custom_data                     = base64encode("#!/bin/bash\nsudo apt update && sudo apt install nginx -y\necho 'Hello from shared WEB' | sudo tee /var/www/html/index.html")

  network_interface_ids = [
    azurerm_network_interface.web.id,
  ]

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

  boot_diagnostics {
    storage_account_uri = azurerm_storage_account.web.primary_blob_endpoint
  }
}



