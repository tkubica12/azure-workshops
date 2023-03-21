resource "azurerm_log_analytics_workspace" "main" {
  name                = random_string.storage.result
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_monitor_diagnostic_setting" "main" {
  name                           = "main"
  target_resource_id             = "${azurerm_storage_account.main.id}/fileServices/default"
  log_analytics_workspace_id     = azurerm_log_analytics_workspace.main.id
  log_analytics_destination_type = "Dedicated"

  enabled_log {
    category = "StorageRead"

    retention_policy {
      enabled = false
    }
  }
  enabled_log {
    category = "StorageWrite"

    retention_policy {
      enabled = false
    }
  }
  enabled_log {
    category = "StorageDelete"

    retention_policy {
      enabled = false
    }
  }
}
