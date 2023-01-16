resource "azurerm_monitor_metric_alert" "connection_a2a_failure" {
  name                = "conn-a2a-failure-alert"
  resource_group_name = azurerm_resource_group.main.name
  scopes              = [azurerm_network_connection_monitor.agent2agent.id]
  window_size         = "PT1M" # What time window to base average on
  frequency           = "PT1M" # How often evaluate

  criteria {
    metric_namespace = "Microsoft.Network/networkWatchers/connectionMonitors"
    metric_name      = "ChecksFailedPercent"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 5
  }

  action {
    action_group_id = azurerm_monitor_action_group.main.id

    webhook_properties = {
      from = "my_a2a_connection"
    }
  }
}

resource "azurerm_monitor_metric_alert" "connection_a2a_rtt" {
  name                = "conn-a2a-rtt-alert"
  resource_group_name = azurerm_resource_group.main.name
  scopes              = [azurerm_network_connection_monitor.agent2agent.id]
  window_size         = "PT1M" # What time window to base average on
  frequency           = "PT1M" # How often evaluate

  criteria {
    metric_namespace = "Microsoft.Network/networkWatchers/connectionMonitors"
    metric_name      = "RoundTripTimeMs"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 200
  }

  action {
    action_group_id = azurerm_monitor_action_group.main.id

    webhook_properties = {
      from = "my_a2a_connection"
    }
  }
}
