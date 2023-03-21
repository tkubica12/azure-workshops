resource "azurerm_log_analytics_workspace" "main" {
  name                = random_string.storage.result
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_monitor_diagnostic_setting" "blob" {
  name                           = "blob"
  target_resource_id             = "${azurerm_storage_account.blob.id}/blobServices/default"
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

resource "azurerm_monitor_diagnostic_setting" "lake" {
  name                           = "lage"
  target_resource_id             = "${azurerm_storage_account.lake.id}/blobServices/default"
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
