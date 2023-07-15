resource "azurerm_monitor_workspace" "main" {
  name                = random_string.main.result
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
}

resource "azurerm_dashboard_grafana" "main" {
  name                              = random_string.main.result
  resource_group_name               = azurerm_resource_group.main.name
  location                          = azurerm_resource_group.main.location
  api_key_enabled                   = true
  deterministic_outbound_ip_enabled = false
  public_network_access_enabled     = true

  azure_monitor_workspace_integrations {
    resource_id = azurerm_monitor_workspace.main.id
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_log_analytics_workspace" "main" {
  name                = random_string.main.result
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

# data "azurerm_monitor_data_collection_endpoint" "main" {
#   name                = azurerm_monitor_workspace.main.name
#   resource_group_name = azurerm_monitor_workspace.main.resource_group_name
# }

# resource "azurerm_monitor_data_collection_rule" "main" {
#   name                        = "aks-to-prometheus"
#   resource_group_name         = azurerm_resource_group.main.name
#   location                    = azurerm_resource_group.main.location
#   data_collection_endpoint_id = data.azurerm_monitor_data_collection_endpoint.main.logs_ingestion_endpoint

#   destinations {
#     log_analytics {
#       workspace_resource_id = azurerm_log_analytics_workspace.example.id
#       name                  = "example-destination-log"
#     }

#     event_hub {
#       event_hub_id = azurerm_eventhub.example.id
#       name         = "example-destination-eventhub"
#     }

#     storage_blob {
#       storage_account_id = azurerm_storage_account.example.id
#       container_name     = azurerm_storage_container.example.name
#       name               = "example-destination-storage"
#     }

#     azure_monitor_metrics {
#       name = "example-destination-metrics"
#     }
#   }

#   data_flow {
#     streams      = ["Microsoft-InsightsMetrics"]
#     destinations = ["example-destination-metrics"]
#   }

#   data_flow {
#     streams      = ["Microsoft-InsightsMetrics", "Microsoft-Syslog", "Microsoft-Perf"]
#     destinations = ["example-destination-log"]
#   }

#   data_flow {
#     streams       = ["Custom-MyTableRawData"]
#     destinations  = ["example-destination-log"]
#     output_stream = "Microsoft-Syslog"
#     transform_kql = "source | project TimeGenerated = Time, Computer, Message = AdditionalContext"
#   }

#   data_sources {
#     syslog {
#       facility_names = ["*"]
#       log_levels     = ["*"]
#       name           = "example-datasource-syslog"
#     }

#     iis_log {
#       streams         = ["Microsoft-W3CIISLog"]
#       name            = "example-datasource-iis"
#       log_directories = ["C:\\Logs\\W3SVC1"]
#     }

#     log_file {
#       name          = "example-datasource-logfile"
#       format        = "text"
#       streams       = ["Custom-MyTableRawData"]
#       file_patterns = ["C:\\JavaLogs\\*.log"]
#       settings {
#         text {
#           record_start_timestamp_format = "ISO 8601"
#         }
#       }
#     }

#     performance_counter {
#       streams                       = ["Microsoft-Perf", "Microsoft-InsightsMetrics"]
#       sampling_frequency_in_seconds = 60
#       counter_specifiers            = ["Processor(*)\\% Processor Time"]
#       name                          = "example-datasource-perfcounter"
#     }

#     windows_event_log {
#       streams        = ["Microsoft-WindowsEvent"]
#       x_path_queries = ["*![System/Level=1]"]
#       name           = "example-datasource-wineventlog"
#     }

#     extension {
#       streams            = ["Microsoft-WindowsEvent"]
#       input_data_sources = ["example-datasource-wineventlog"]
#       extension_name     = "example-extension-name"
#       extension_json = jsonencode({
#         a = 1
#         b = "hello"
#       })
#       name = "example-datasource-extension"
#     }
#   }

#   stream_declaration {
#     stream_name = "Custom-MyTableRawData"
#     column {
#       name = "Time"
#       type = "datetime"
#     }
#     column {
#       name = "Computer"
#       type = "string"
#     }
#     column {
#       name = "AdditionalContext"
#       type = "string"
#     }
#   }

#   identity {
#     type         = "UserAssigned"
#     identity_ids = [azurerm_user_assigned_identity.example.id]
#   }

#   description = "data collection rule example"
#   tags = {
#     foo = "bar"
#   }
#   depends_on = [
#     azurerm_log_analytics_solution.example
#   ]
# }