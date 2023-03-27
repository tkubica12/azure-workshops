// Blob storage account
resource "azurerm_storage_account" "blob" {
  name                            = "blob${random_string.storage.result}"
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

// Assign current user Storage Blob Data Owner role
resource "azurerm_role_assignment" "storage_blob_tf" {
  scope                = azurerm_storage_account.blob.id
  role_definition_name = "Storage Blob Data Owner"
  principal_id         = data.azurerm_client_config.current.object_id
}

// Team1 container
resource "azurerm_storage_container" "team1" {
  name                  = "team1"
  storage_account_name  = azurerm_storage_account.blob.name
  container_access_type = "private"
}

// Team2 container
resource "azurerm_storage_container" "team2" {
  name                  = "team2"
  storage_account_name  = azurerm_storage_account.blob.name
  container_access_type = "private"
}

// Dataplane RBAC assignments
resource "azurerm_role_assignment" "storage_blob_team1" {
  scope                = "${azurerm_storage_account.blob.id}/blobServices/default/containers/${azurerm_storage_container.team1.name}"
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.identity1.principal_id
}

resource "azurerm_role_assignment" "storage_blob_team2" {
  scope                = "${azurerm_storage_account.blob.id}/blobServices/default/containers/${azurerm_storage_container.team2.name}"
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.identity2.principal_id
}

// Controlplane RBAC assignments
resource "azurerm_role_assignment" "storage_account_blob_team1" {
  scope                = azurerm_storage_account.blob.id
  role_definition_name = "Reader"
  principal_id         = azurerm_user_assigned_identity.identity1.principal_id
}

resource "azurerm_role_assignment" "storage_account_blob_team2" {
  scope                = azurerm_storage_account.blob.id
  role_definition_name = "Reader"
  principal_id         = azurerm_user_assigned_identity.identity2.principal_id
}