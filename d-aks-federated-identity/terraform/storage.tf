resource "random_string" "main" {
  length  = 16
  lower   = true
  upper   = false
  special = false
  numeric = false
}

resource "azurerm_storage_account" "main" {
  name                     = random_string.main.result
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "main" {
  name                 = "container"
  storage_account_name = azurerm_storage_account.main.name
}

resource "azurerm_storage_blob" "main" {
  name                   = "file.txt"
  storage_account_name   = azurerm_storage_account.main.name
  storage_container_name = azurerm_storage_container.main.name
  type                   = "Block"
  source_content         = "My super data file"
}


resource "azurerm_role_assignment" "main" {
  role_definition_name = "Storage Blob Data Reader"
  scope                = azurerm_storage_account.main.id
  principal_id         = azurerm_user_assigned_identity.identity1.principal_id
}
