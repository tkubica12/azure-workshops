resource "azurerm_network_interface" "vm_ade" {
  name                = "vm-ade-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_windows_virtual_machine" "vm_ade" {
  name                = "vm-ade"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = "Standard_B2ms"
  admin_username      = "tomas"
  admin_password      = "Azure12345678"

  network_interface_ids = [
    azurerm_network_interface.vm_ade.id,
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2019-Datacenter"
    version   = "latest"
  }
}

resource "azurerm_key_vault_key" "vm_ade" {
  name         = "key-ade"
  key_vault_id = azurerm_key_vault.main.id
  key_type     = "RSA"
  key_size     = 2048

  depends_on = [
    azurerm_key_vault_access_policy.main
  ]

  key_opts = [
    "decrypt",
    "encrypt",
    "sign",
    "unwrapKey",
    "verify",
    "wrapKey",
  ]
}

resource "azurerm_virtual_machine_extension" "vm_ade" {
  name                       = "AzureDiskEncryption"
  virtual_machine_id         = azurerm_windows_virtual_machine.vm_ade.id
  publisher                  = "Microsoft.Azure.Security"
  type                       = "AzureDiskEncryption"
  type_handler_version       = "2.2"
  auto_upgrade_minor_version = true

  settings = <<SETTINGS
    {
        "EncryptionOperation"         :     "EnableEncryption",
        "KeyVaultURL"                 :     "${azurerm_key_vault.main.vault_uri}",
        "KeyVaultResourceId"          :     "${azurerm_key_vault.main.id}",
        "KeyEncryptionKeyURL"         :     "${azurerm_key_vault_key.vm_ade.id}",
        "KekVaultResourceId"          :     "${azurerm_key_vault.main.id}",
        "KeyEncryptionAlgorithm"      :     "RSA-OAEP",
        "VolumeType"                  :     "All"
    }
    SETTINGS

    depends_on = [
      azurerm_key_vault_key.vm_ade,
    ]
}
