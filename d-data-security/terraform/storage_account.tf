resource "azurerm_storage_account" "main" {
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
  storage_account_id = azurerm_storage_account.main.id
  key_vault_id       = azurerm_key_vault.main.id
  key_name           = azurerm_key_vault_key.storageaccount.name
}

resource "azurerm_key_vault_access_policy" "storage" {
  key_vault_id = azurerm_key_vault.main.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_storage_account.main.identity.0.principal_id

  key_permissions    = ["Get", "Create", "List", "Restore", "Recover", "UnwrapKey", "WrapKey", "Purge", "Encrypt", "Decrypt", "Sign", "Verify"]
  secret_permissions = ["Get"]
}

resource "azurerm_key_vault_key" "storageaccount" {
  name         = "key-storageaccount"
  key_vault_id = azurerm_key_vault.main.id
  key_type     = "RSA"
  key_size     = 2048
  key_opts     = ["decrypt", "encrypt", "sign", "unwrapKey", "verify", "wrapKey"]

  depends_on = [
    azurerm_key_vault_access_policy.main,
    azurerm_key_vault_access_policy.storage,
  ]
}
