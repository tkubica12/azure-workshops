// Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "main" {
  name                = random_string.main.result
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

// Storage Accounts
resource "azurerm_storage_account" "location1" {
  name                      = "${random_string.main.result}l1"
  resource_group_name       = azurerm_resource_group.main.name
  location                  = azurerm_resource_group.main.location
  account_tier              = "Standard"
  account_kind              = "StorageV2"
  account_replication_type  = "LRS"
  enable_https_traffic_only = true
}

resource "azurerm_storage_account" "location2" {
  name                      = "${random_string.main.result}l2"
  resource_group_name       = azurerm_resource_group.main.name
  location                  = var.location2
  account_tier              = "Standard"
  account_kind              = "StorageV2"
  account_replication_type  = "LRS"
  enable_https_traffic_only = true
}

// Network Watcher
resource "azurerm_network_watcher" "location1" {
  count               = var.existing_watcher_name_location1 == "" ? 1 : 0
  name                = "net-watcher-${var.location1}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_network_watcher" "location2" {
  count               = var.existing_watcher_name_location2 == "" ? 1 : 0
  name                = "net-watcher-${var.location2}"
  location            = var.location2
  resource_group_name = azurerm_resource_group.main.name
}

locals {
  network_watcher_name_location1 = var.existing_watcher_name_location1 == "" ? azurerm_network_watcher.location1[0].name : var.existing_watcher_name_location1
  network_watcher_name_location2 = var.existing_watcher_name_location2 == "" ? azurerm_network_watcher.location2[0].name : var.existing_watcher_name_location2
  network_watcher_rg_location1   = var.existing_watcher_rg_location1 == "" ? azurerm_resource_group.main.name : var.existing_watcher_rg_location1
  network_watcher_rg_location2   = var.existing_watcher_rg_location2 == "" ? azurerm_resource_group.main.name : var.existing_watcher_rg_location2
}
