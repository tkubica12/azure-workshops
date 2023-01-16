// NICs
resource "azurerm_network_interface" "nic_location1" {
  name                = "nic-${var.location1}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  ip_configuration {
    name                          = "ipconfig01"
    subnet_id                     = azurerm_subnet.location1.id
    private_ip_address_allocation = "Static"
    private_ip_address            = "10.0.0.10"
  }
}

resource "azurerm_network_interface" "nic_location2" {
  name                = "nic-${var.location2}"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location2

  ip_configuration {
    name                          = "ipconfig01"
    subnet_id                     = azurerm_subnet.location2.id
    private_ip_address_allocation = "Static"
    private_ip_address            = "10.1.0.10"
  }
}

// VMs
resource "azurerm_windows_virtual_machine" "vm_location1" {
  name                            = "vm-${var.location1}"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  size                            = "Standard_B2ms"
  admin_username                  = "tomas"
  admin_password                  = var.admin_password
  network_interface_ids           = [azurerm_network_interface.nic_location1.id]

  source_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2019-Datacenter"
    version   = "latest"
  }

  os_disk {
    name                 = "disk-${var.location1}-${random_string.main.result}"
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  boot_diagnostics {}
}

resource "azurerm_windows_virtual_machine" "vm_location2" {
  name                            = "vm-${var.location2}"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = var.location2
  size                            = "Standard_B2ms"
  admin_username                  = "tomas"
  admin_password                  = var.admin_password
  network_interface_ids           = [azurerm_network_interface.nic_location2.id]

  source_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2019-Datacenter"
    version   = "latest"
  }

  os_disk {
    name                 = "disk-${var.location2}-${random_string.main.result}"
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  boot_diagnostics {}
}

// Network Watcher extensions for VM (for machines outside of Azure you canboard with Azure Arc or even install agent manually)
resource "azurerm_virtual_machine_extension" "location1" {
  name                       = "network-watcher"
  virtual_machine_id         = azurerm_windows_virtual_machine.vm_location1.id
  publisher                  = "Microsoft.Azure.NetworkWatcher"
  type                       = "NetworkWatcherAgentWindows"
  type_handler_version       = "1.4"
  auto_upgrade_minor_version = true
}

resource "azurerm_virtual_machine_extension" "location2" {
  name                       = "network-watcher"
  virtual_machine_id         = azurerm_windows_virtual_machine.vm_location2.id
  publisher                  = "Microsoft.Azure.NetworkWatcher"
  type                       = "NetworkWatcherAgentWindows"
  type_handler_version       = "1.4"
  auto_upgrade_minor_version = true
}