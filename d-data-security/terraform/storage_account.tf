resource "azurerm_storage_account" "main" {
  count                             = var.enable_storage ? 1 : 0
  name                              = random_string.main.result
  resource_group_name               = azurerm_resource_group.main.name
  location                          = azurerm_resource_group.main.location
  account_tier                      = "Standard"
  account_replication_type          = "LRS"
  account_kind                      = "StorageV2"
  infrastructure_encryption_enabled = true

  immutability_policy {
    state                         = "Unlocked"
    allow_protected_append_writes = false
    period_since_creation_in_days = 1
  }

  blob_properties {
    versioning_enabled       = true
    last_access_time_enabled = true
    change_feed_enabled      = true
  }

  identity {
    type = "SystemAssigned"
  }

  lifecycle {
    ignore_changes = [
      customer_managed_key
    ]
  }
}

resource "azurerm_storage_account_customer_managed_key" "main" {
  count              = var.enable_storage ? 1 : 0
  storage_account_id = azurerm_storage_account.main[0].id
  key_vault_id       = azurerm_key_vault.main.id
  key_name           = azurerm_key_vault_key.storageaccount[0].name

  depends_on = [
    azurerm_role_assignment.kv_storage
  ]
}

resource "azurerm_role_assignment" "kv_storage" {
  count                = var.enable_storage ? 1 : 0
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Crypto Service Encryption User"
  principal_id         = azurerm_storage_account.main[0].identity.0.principal_id
}

resource "azurerm_key_vault_key" "storageaccount" {
  count        = var.enable_storage ? 1 : 0
  name         = "key-storageaccount"
  key_vault_id = azurerm_key_vault.main.id
  key_type     = "RSA"
  key_size     = 2048
  key_opts     = ["decrypt", "encrypt", "sign", "unwrapKey", "verify", "wrapKey"]

  depends_on = [
    azurerm_role_assignment.kv_main,
  ]
}
