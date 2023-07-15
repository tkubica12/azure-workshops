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

resource "azurerm_role_assignment" "grafana" {
  scope                = azurerm_dashboard_grafana.main.id
  role_definition_name = "Grafana Admin"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_log_analytics_workspace" "main" {
  name                = random_string.main.result
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

# data "azapi_resource" "azurerm_monitor_workspace" {
#   name      = azurerm_monitor_workspace.main.name
#   parent_id = azurerm_resource_group.main.id
#   type      = "microsoft.monitor/accounts@2021-06-03-preview"

#   response_export_values = ["*"]
# }

resource "azurerm_monitor_data_collection_endpoint" "main" {
  name                          = "aks-endpoint"
  resource_group_name           = azurerm_resource_group.main.name
  location                      = azurerm_resource_group.main.location
  kind                          = "Linux"
  public_network_access_enabled = true
}

resource "azurerm_monitor_data_collection_rule" "main" {
  name                        = "aks-to-prometheus"
  resource_group_name         = azurerm_resource_group.main.name
  location                    = azurerm_resource_group.main.location
  data_collection_endpoint_id = azurerm_monitor_data_collection_endpoint.main.id

  destinations {
    monitor_account {
      monitor_account_id = azurerm_monitor_workspace.main.id
      name               = "MonitoringAccount1"
    }
  }

  data_flow {
    streams      = ["Microsoft-PrometheusMetrics"]
    destinations = ["MonitoringAccount1"]
  }

  data_sources {
    prometheus_forwarder {
      name = "PrometheusDataSource"
      streams = [ "Microsoft-PrometheusMetrics" ]
    }
  }

  depends_on = [
    azurerm_monitor_workspace.main
  ]
}

resource "azurerm_monitor_data_collection_rule_association" "aks1" {
  target_resource_id          = azurerm_kubernetes_cluster.aks1.id
  data_collection_endpoint_id = azurerm_monitor_data_collection_endpoint.main.id
  description                 = "aks1"
}