resource "azurerm_monitor_metric_alert" "cpu" {
  name                = "nva-cpu-alert"
  resource_group_name = azurerm_resource_group.main.name
  scopes              = [azurerm_windows_virtual_machine.vm_location1.id]
  window_size         = "PT1M" # What time window to base average on
  frequency           = "PT1M" # How often evaluate

  criteria {
    metric_namespace = "Microsoft.Compute/virtualMachines"
    metric_name      = "Percentage CPU"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 20
  }

  action {
    action_group_id = azurerm_monitor_action_group.main.id

    webhook_properties = {
      from = "my_nva_location1"
    }
  }
}
