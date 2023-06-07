resource "azurerm_storage_account" "files" {
  name                     = "files${random_string.main.result}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_share" "main" {
  name                 = "myshare"
  storage_account_name = azurerm_storage_account.files.name
  quota                = 50
}

resource "azurerm_storage_share_directory" "dir1" {
  name                 = "dir1"
  share_name           = azurerm_storage_share.main.name
  storage_account_name = azurerm_storage_account.files.name
}

resource "azurerm_storage_share_directory" "dir2" {
  name                 = "dir2"
  share_name           = azurerm_storage_share.main.name
  storage_account_name = azurerm_storage_account.files.name
}

