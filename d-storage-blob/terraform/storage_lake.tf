// Data Lake Gen2 storage account
resource "azurerm_storage_account" "lake" {
  name                            = "lake${random_string.storage.result}"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  account_tier                    = "Standard"
  account_replication_type        = "RAGZRS"
  shared_access_key_enabled       = true
  default_to_oauth_authentication = false
  is_hns_enabled                  = true
}

// Assign current user Storage Blob Data Owner role
resource "azurerm_role_assignment" "storage_lake_tf" {
  scope                = azurerm_storage_account.lake.id
  role_definition_name = "Storage Blob Data Owner"
  principal_id         = data.azurerm_client_config.current.object_id
}

// Team1 file system
resource "azurerm_storage_data_lake_gen2_filesystem" "team1" {
  name               = "team1"
  storage_account_id = azurerm_storage_account.lake.id
}

// Team2 file system
resource "azurerm_storage_data_lake_gen2_filesystem" "team2" {
  name               = "team2"
  storage_account_id = azurerm_storage_account.lake.id
}

// Team1 folder1
resource "azurerm_storage_data_lake_gen2_path" "team1_folder1" {
  path               = "folder1"
  filesystem_name    = azurerm_storage_data_lake_gen2_filesystem.team1.name
  storage_account_id = azurerm_storage_account.lake.id
  resource           = "directory"

  ace {
    scope       = "access"
    type        = "user"
    id          = azurerm_user_assigned_identity.identity1.principal_id
    permissions = "rwx"
  }

  ace {
    scope       = "default"
    type        = "user"
    id          = azurerm_user_assigned_identity.identity1.principal_id
    permissions = "rwx"
  }

  depends_on = [
    azurerm_role_assignment.storage_lake_tf
  ]
}

// Team1 folder2
resource "azurerm_storage_data_lake_gen2_path" "team1_folder2" {
  path               = "folder2"
  filesystem_name    = azurerm_storage_data_lake_gen2_filesystem.team1.name
  storage_account_id = azurerm_storage_account.lake.id
  resource           = "directory"

  depends_on = [
    azurerm_role_assignment.storage_lake_tf
  ]
}

// Team2 folder1
resource "azurerm_storage_data_lake_gen2_path" "team2_folder1" {
  path               = "folder1"
  filesystem_name    = azurerm_storage_data_lake_gen2_filesystem.team2.name
  storage_account_id = azurerm_storage_account.lake.id
  resource           = "directory"

  depends_on = [
    azurerm_role_assignment.storage_lake_tf
  ]
}

// Team2 folder2
resource "azurerm_storage_data_lake_gen2_path" "team2_folder2" {
  path               = "folder2"
  filesystem_name    = azurerm_storage_data_lake_gen2_filesystem.team2.name
  storage_account_id = azurerm_storage_account.lake.id
  resource           = "directory"

  depends_on = [
    azurerm_role_assignment.storage_lake_tf
  ]
}

// Team1 folder1 subfolder1
resource "azurerm_storage_data_lake_gen2_path" "team1_folder1_subfolder1" {
  path               = "folder1/subfolder1"
  filesystem_name    = azurerm_storage_data_lake_gen2_filesystem.team1.name
  storage_account_id = azurerm_storage_account.lake.id
  resource           = "directory"

  ace {
    scope       = "access"
    type        = "user"
    id          = azurerm_user_assigned_identity.identity2.principal_id
    permissions = "r-x"
  }

  depends_on = [
    azurerm_role_assignment.storage_lake_tf,
    azurerm_storage_data_lake_gen2_path.team1_folder1
  ]
}
