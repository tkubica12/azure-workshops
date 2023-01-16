resource "azurerm_monitor_activity_log_alert" "main" {
  name                = "nva-resourcehelaht-alert"
  resource_group_name = azurerm_resource_group.main.name

  scopes = [
    azurerm_windows_virtual_machine.vm_location1.id,
    azurerm_windows_virtual_machine.vm_location2.id
  ]

  criteria {
    category       = "ResourceHealth"
  }

  action {
    action_group_id = azurerm_monitor_action_group.main.id

    webhook_properties = {
      from = "my_nva_location1"
    }
  }
}
