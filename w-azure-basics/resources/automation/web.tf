resource "azurerm_network_interface" "web" {
  count               = var.serverCount
  name                = "web-nic${count.index}"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.demo.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_network_interface_backend_address_pool_association" "web" {
  count                   = var.serverCount
  network_interface_id    = azurerm_network_interface.web[count.index].id
  ip_configuration_name   = "internal"
  backend_address_pool_id = azurerm_lb_backend_address_pool.demo.id
}

resource "azurerm_linux_virtual_machine" "web" {
  count                           = var.serverCount
  name                            = "web-vm${count.index}"
  resource_group_name             = azurerm_resource_group.demo.name
  location                        = azurerm_resource_group.demo.location
  size                            = "Standard_B1ms"
  admin_username                  = "tomas"
  admin_password                  = var.password
  disable_password_authentication = false
  custom_data                     = base64encode("#!/bin/bash\nsudo apt update && sudo apt install nginx -y\necho 'Hello from shared WEB ${count.index}' | sudo tee /var/www/html/index.html")

  network_interface_ids = [
    azurerm_network_interface.web[count.index].id,
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

resource "azurerm_storage_account" "web" {
  name                     = "${var.prefix}542"
  resource_group_name      = azurerm_resource_group.demo.name
  location                 = azurerm_resource_group.demo.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}



