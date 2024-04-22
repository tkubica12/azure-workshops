resource "azurerm_storage_account" "main" {
  name                     = module.naming.storage_account.name_unique
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "ZRS"
  account_kind             = "StorageV2"
}

resource "azurerm_storage_share" "main" {
  name                 = "myshare"
  storage_account_name = azurerm_storage_account.main.name
  quota                = 50
}

resource "azurerm_storage_share_file" "index" {
  name             = "index.html"
  storage_share_id = azurerm_storage_share.main.id
  source           = "${path.module}/starter_site/index.html"
}