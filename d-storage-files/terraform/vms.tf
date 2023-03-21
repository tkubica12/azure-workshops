resource "azurerm_network_interface" "vm1" {
  name                = "user1-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_servers         = azurerm_active_directory_domain_service.main.initial_replica_set[0].domain_controller_ip_addresses

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.vm.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_windows_virtual_machine" "vm1" {
  name                = "user1"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = "Standard_D2as_v4"
  admin_username      = "tomas"
  admin_password      = "Azure12345678"

  network_interface_ids = [
    azurerm_network_interface.vm1.id,
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2022-Datacenter"
    version   = "latest"
  }

  depends_on = [
    azurerm_active_directory_domain_service.main
  ]
}

resource "azurerm_virtual_machine_extension" "vm1_domainjoin" {
  name                 = "domainjoin"
  virtual_machine_id   = azurerm_windows_virtual_machine.vm1.id
  publisher            = "Microsoft.Compute"
  type                 = "JsonADDomainExtension"
  type_handler_version = "1.3"

  settings = <<SETTINGS
    {
    "Name": "tkubica.biz",
    "User": "${azuread_user.user1.user_principal_name}",
    "Restart": "true",
    "Options": "3"
    }
    SETTINGS

  protected_settings = <<PROTECTED_SETTINGS
    {
    "Password": "${random_password.users.result}"
    }
    PROTECTED_SETTINGS
}

resource "azurerm_network_interface" "vm2" {
  name                = "user2-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_servers         = azurerm_active_directory_domain_service.main.initial_replica_set[0].domain_controller_ip_addresses

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.vm.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_windows_virtual_machine" "vm2" {
  name                = "user2"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = "Standard_D2as_v4"
  admin_username      = "tomas"
  admin_password      = "Azure12345678"

  network_interface_ids = [
    azurerm_network_interface.vm2.id,
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2022-Datacenter"
    version   = "latest"
  }

  depends_on = [
    azurerm_active_directory_domain_service.main
  ]
}

resource "azurerm_virtual_machine_extension" "vm2_domainjoin" {
  name                 = "domainjoin"
  virtual_machine_id   = azurerm_windows_virtual_machine.vm2.id
  publisher            = "Microsoft.Compute"
  type                 = "JsonADDomainExtension"
  type_handler_version = "1.3"

  settings = <<SETTINGS
    {
    "Name": "tkubica.biz",
    "User": "${azuread_user.user2.user_principal_name}",
    "Restart": "true",
    "Options": "3"
    }
    SETTINGS

  protected_settings = <<PROTECTED_SETTINGS
    {
    "Password": "${random_password.users.result}"
    }
    PROTECTED_SETTINGS
}

resource "azurerm_network_interface" "vm3" {
  name                = "admin-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_servers         = azurerm_active_directory_domain_service.main.initial_replica_set[0].domain_controller_ip_addresses

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.vm.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_windows_virtual_machine" "vm3" {
  name                = "fadmin"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = "Standard_D2as_v4"
  admin_username      = "tomas"
  admin_password      = "Azure12345678"

  network_interface_ids = [
    azurerm_network_interface.vm3.id,
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2022-Datacenter"
    version   = "latest"
  }

  depends_on = [
    azurerm_active_directory_domain_service.main
  ]
}

resource "azurerm_virtual_machine_extension" "vm3_domainjoin" {
  name                 = "domainjoin"
  virtual_machine_id   = azurerm_windows_virtual_machine.vm3.id
  publisher            = "Microsoft.Compute"
  type                 = "JsonADDomainExtension"
  type_handler_version = "1.3"

  settings = <<SETTINGS
    {
    "Name": "tkubica.biz",
    "User": "${azuread_user.admin.user_principal_name}",
    "Restart": "true",
    "Options": "3"
    }
    SETTINGS

  protected_settings = <<PROTECTED_SETTINGS
    {
    "Password": "${random_password.users.result}"
    }
    PROTECTED_SETTINGS
}
