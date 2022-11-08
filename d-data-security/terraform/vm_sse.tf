resource "azurerm_network_interface" "vm_sse" {
  name                = "vm_sse-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_windows_virtual_machine" "vm_sse" {
  name                       = "vm-sse"
  resource_group_name        = azurerm_resource_group.main.name
  location                   = azurerm_resource_group.main.location
  size                       = "Standard_B2ms"
  admin_username             = "tomas"
  admin_password             = "Azure12345678"
  encryption_at_host_enabled = true

  network_interface_ids = [
    azurerm_network_interface.vm_sse.id,
  ]

  os_disk {
    caching                = "ReadWrite"
    storage_account_type   = "Standard_LRS"
    disk_encryption_set_id = azurerm_disk_encryption_set.sse.id
  }

  source_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2019-Datacenter"
    version   = "latest"
  }

  depends_on = [
    azurerm_key_vault_access_policy.sse,
    azurerm_key_vault_key.sse,
  ]
}

resource "azurerm_key_vault_key" "sse" {
  name         = "key-sse"
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

resource "azurerm_key_vault_access_policy" "sse" {
  key_vault_id = azurerm_key_vault.main.id

  tenant_id = azurerm_disk_encryption_set.sse.identity.0.tenant_id
  object_id = azurerm_disk_encryption_set.sse.identity.0.principal_id

  key_permissions = [
    "WrapKey",
    "UnwrapKey",
    "Get"
  ]
}


resource "azurerm_disk_encryption_set" "sse" {
  name                = "sse-encryption-set"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  key_vault_key_id    = azurerm_key_vault_key.sse.id
  encryption_type     = "EncryptionAtRestWithPlatformAndCustomerKeys"

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_role_assignment" "sse" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Crypto Service Encryption User"
  principal_id         = azurerm_disk_encryption_set.sse.identity.0.principal_id
}

resource "azurerm_managed_disk" "sse" {
  name                   = "data-disk-sse"
  location               = azurerm_resource_group.main.location
  resource_group_name    = azurerm_resource_group.main.name
  storage_account_type   = "Standard_LRS"
  create_option          = "Empty"
  disk_size_gb           = "32"
  disk_encryption_set_id = azurerm_disk_encryption_set.sse.id

  depends_on = [
    azurerm_role_assignment.sse,
    azurerm_key_vault_access_policy.sse
  ]
}
