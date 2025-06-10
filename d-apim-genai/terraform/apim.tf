resource "azurerm_api_management" "main" {
  name                = "apim-${local.base_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  publisher_name      = "My Company"
  publisher_email     = "company@company.local"
  sku_name            = var.apim_sku

  identity {
    type         = "SystemAssigned"
  }
}

resource "azurerm_api_management_logger" "main" {
  name                = "main"
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  resource_id         = azurerm_application_insights.main.id

  application_insights {
    instrumentation_key = azurerm_application_insights.main.instrumentation_key
  }
}

resource "azurerm_api_management_redis_cache" "main" {
  name              = "default"
  api_management_id = azurerm_api_management.main.id
  connection_string = local.redis_connection_string
}


resource "azurerm_monitor_diagnostic_setting" "main" {
  name               = "main"
  target_resource_id = azurerm_api_management.main.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id

  # enabled_log {
  #   category = "AuditEvent"
  # }

  metric {
    category = "AllMetrics"
  }
}

