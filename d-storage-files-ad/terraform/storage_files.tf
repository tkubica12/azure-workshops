resource "azurerm_storage_account" "main" {
  name                     = random_string.storage.result
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  lifecycle {
    ignore_changes = [
      azure_files_authentication
    ]
  }
}

resource "azurerm_storage_share" "share1" {
  name                 = "share1"
  storage_account_name = azurerm_storage_account.main.name
  quota                = 50
}

resource "azurerm_storage_share" "share2" {
  name                 = "share2"
  storage_account_name = azurerm_storage_account.main.name
  quota                = 50
}

resource "azurerm_role_assignment" "share1_user1" {
  scope                = azurerm_storage_share.share1.resource_manager_id
  role_definition_name = "Storage File Data SMB Share Elevated Contributor"
  principal_id         = azuread_user.user1.object_id
}

resource "azurerm_role_assignment" "share1_user2" {
  scope                = azurerm_storage_share.share1.resource_manager_id
  role_definition_name = "Storage File Data SMB Share Reader"
  principal_id         = azuread_user.user2.object_id
}

resource "azurerm_role_assignment" "share2_user2" {
  scope                = azurerm_storage_share.share2.resource_manager_id
  role_definition_name = "Storage File Data SMB Share Elevated Contributor"
  principal_id         = azuread_user.user2.object_id
}


