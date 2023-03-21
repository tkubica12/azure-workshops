resource "azurerm_storage_account" "main" {
  name                            = random_string.main.result
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  account_tier                    = "Standard"
  account_replication_type        = "RAGZRS"
  shared_access_key_enabled       = true
  default_to_oauth_authentication = false
  is_hns_enabled                  = false

  blob_properties {
    change_feed_enabled = true
    versioning_enabled  = true
  }
}

resource "azurerm_storage_share" "main" {
  name                 = "myshare"
  storage_account_name = azurerm_storage_account.main.name
  quota                = 50
}

resource "azurerm_role_assignment" "vaulted" {
  scope                = azurerm_storage_account.main.id
  role_definition_name = "Storage Account Backup Contributor"
  principal_id         = azurerm_data_protection_backup_vault.vaulted.identity[0].principal_id
}

# resource "azurerm_role_assignment" "operational" {
#   scope                = azurerm_storage_account.main.id
#   role_definition_name = "Storage Account Backup Contributor"
#   principal_id         = azurerm_data_protection_backup_vault.operational.identity[0].principal_id
# }