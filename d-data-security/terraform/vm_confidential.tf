resource "azurerm_key_vault_key" "vm_confidential" {
  name         = "key-confidentialvm"
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

resource "azurerm_key_vault_access_policy" "vm_confidential" {
  key_vault_id = azurerm_key_vault.main.id

  tenant_id = azurerm_disk_encryption_set.vm_confidential.identity.0.tenant_id
  object_id = azurerm_disk_encryption_set.vm_confidential.identity.0.principal_id

  key_permissions = [
    "WrapKey",
    "UnwrapKey",
    "Get"
  ]
}


resource "azurerm_disk_encryption_set" "vm_confidential" {
  name                = "confidentialvm-encryption-set"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  key_vault_key_id    = azurerm_key_vault_key.vm_confidential.id
  encryption_type     = "ConfidentialVmEncryptedWithCustomerKey"

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_role_assignment" "vm_confidential" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Crypto Service Encryption User"
  principal_id         = azurerm_disk_encryption_set.vm_confidential.identity.0.principal_id
}


resource "azurerm_network_interface" "vm_confidential" {
  name                = "vm-confidential-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_windows_virtual_machine" "vm_confidential" {
  name                = "vm-confidential"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = "Standard_DC2as_v5"
  admin_username      = "tomas"
  admin_password      = "Azure12345678"
  vtpm_enabled        = true
  secure_boot_enabled = true

  network_interface_ids = [
    azurerm_network_interface.vm_confidential.id,
  ]

  os_disk {
    caching                          = "ReadWrite"
    storage_account_type             = "Standard_LRS"
    secure_vm_disk_encryption_set_id = azurerm_disk_encryption_set.vm_confidential.id
    security_encryption_type         = "DiskWithVMGuestState"
  }

  source_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2022-Datacenter-smalldisk-g2"
    version   = "latest"
  }

  depends_on = [
    azurerm_key_vault_access_policy.vm_confidential,
    azurerm_key_vault_key.vm_confidential,
  ]
}

