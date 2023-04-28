resource "azurerm_key_vault_key" "vm_confidential" {
  count        = var.enable_confidential_vm ? 1 : 0
  name         = "key-confidentialvm"
  key_vault_id = azurerm_key_vault.main.id
  key_type     = "RSA"
  key_size     = 2048

  depends_on = [
    azurerm_role_assignment.kv_main
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

resource "azurerm_role_assignment" "kv_vm_confidential" {
  count                = var.enable_confidential_vm ? 1 : 0
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Crypto Service Encryption User"
  principal_id         = azurerm_disk_encryption_set.vm_confidential[0].identity.0.principal_id
}

resource "azurerm_disk_encryption_set" "vm_confidential" {
  count               = var.enable_confidential_vm ? 1 : 0
  name                = "confidentialvm-encryption-set"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  key_vault_key_id    = azurerm_key_vault_key.vm_confidential[0].id
  encryption_type     = "ConfidentialVmEncryptedWithCustomerKey"

  identity {
    type = "SystemAssigned"
  }
}

// Windows on AMD
resource "azurerm_network_interface" "vm_win_amd_confidential" {
  count               = var.enable_confidential_vm ? 1 : 0
  name                = "vm-win-amd-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_windows_virtual_machine" "vm_win_amd_confidential" {
  count               = var.enable_confidential_vm ? 1 : 0
  name                = "vm-win-amd"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = "Standard_DC2as_v5"
  admin_username      = "tomas"
  admin_password      = "Azure12345678"
  vtpm_enabled        = true
  secure_boot_enabled = true

  network_interface_ids = [
    azurerm_network_interface.vm_win_amd_confidential[0].id,
  ]

  os_disk {
    caching                          = "ReadWrite"
    storage_account_type             = "Standard_LRS"
    secure_vm_disk_encryption_set_id = azurerm_disk_encryption_set.vm_confidential[0].id
    security_encryption_type         = "DiskWithVMGuestState"
  }

  source_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2022-Datacenter-smalldisk-g2"
    version   = "latest"
  }

  depends_on = [
    azurerm_role_assignment.kv_vm_confidential[0],
    azurerm_key_vault_key.vm_confidential[0],
  ]
}

// Linux on AMD
resource "azurerm_network_interface" "vm_linux_amd_confidential" {
  count               = var.enable_confidential_vm ? 1 : 0
  name                = "vm-linux-amd-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_linux_virtual_machine" "vm_linux_amd_confidential" {
  count                           = var.enable_confidential_vm ? 1 : 0
  name                            = "vm-linux-amd"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  size                            = "Standard_DC2as_v5"
  admin_username                  = "tomas"
  admin_password                  = "Azure12345678"
  vtpm_enabled                    = true
  secure_boot_enabled             = true
  disable_password_authentication = false

  network_interface_ids = [
    azurerm_network_interface.vm_linux_amd_confidential[0].id,
  ]

  os_disk {
    caching                          = "ReadWrite"
    storage_account_type             = "Standard_LRS"
    secure_vm_disk_encryption_set_id = azurerm_disk_encryption_set.vm_confidential[0].id
    security_encryption_type         = "DiskWithVMGuestState"
  }

  source_image_reference {
    publisher = "canonical"
    offer     = "0001-com-ubuntu-confidential-vm-focal"
    sku       = "20_04-lts-cvm"
    version   = "latest"
  }

  depends_on = [
    azurerm_role_assignment.kv_vm_confidential[0],
    azurerm_key_vault_key.vm_confidential[0],
  ]

}
