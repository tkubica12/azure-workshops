resource "azurerm_log_analytics_workspace" "main" {
  name                = module.naming.log_analytics_workspace.name
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_monitor_data_collection_endpoint" "main" {
  name                = "${var.prefix}-dcre"
  resource_group_name = var.resource_group_name
  location            = var.location

  lifecycle {
    create_before_destroy = true
  }
}

resource "azurerm_monitor_data_collection_rule" "main" {
  name                        = "${var.prefix}-dcr"
  resource_group_name         = var.resource_group_name
  location                    = var.location
  data_collection_endpoint_id = azurerm_monitor_data_collection_endpoint.main.id

  data_sources {
    performance_counter {
      name                          = "VMInsightsPerfCounters"
      streams                       = ["Microsoft-InsightsMetrics"]
      sampling_frequency_in_seconds = 60
      counter_specifiers            = ["\\VmInsights\\DetailedMetrics"]
    }

    extension {
      name           = "DependencyAgentDataSource"
      streams        = ["Microsoft-ServiceMap"]
      extension_name = "DependencyAgent"
    }
  }

  destinations {
    log_analytics {
      name                  = "VMInsightsPerf-Logs-Dest"
      workspace_resource_id = azurerm_log_analytics_workspace.main.id
    }
  }

  data_flow {
    streams      = ["Microsoft-InsightsMetrics"]
    destinations = ["VMInsightsPerf-Logs-Dest"]
  }

  data_flow {
    streams      = ["Microsoft-ServiceMap"]
    destinations = ["VMInsightsPerf-Logs-Dest"]
  }
}

