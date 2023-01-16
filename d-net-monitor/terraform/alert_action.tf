resource "azurerm_monitor_action_group" "main" {
  name                = "d-net-monitor-action-group"
  resource_group_name = azurerm_resource_group.main.name
  short_name          = "dnetmonitor"

  email_receiver {
    name                    = "send_email"
    email_address           = var.email
    use_common_alert_schema = true
  }

  logic_app_receiver {
    name                    = "mylogicapp"
    resource_id             = azurerm_log_analytics_workspace.main.id
    callback_url            = azurerm_logic_app_trigger_http_request.main.callback_url
    use_common_alert_schema = true
  }

  webhook_receiver {
    name                    = "api_call_example"
    service_uri             = "https://webhook.site/020ceeda-a81c-46be-98f0-a7ee21a87057"
    use_common_alert_schema = true
  }
}