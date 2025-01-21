resource "azurerm_role_assignment" "datareaderrole" {
  scope              = azurerm_monitor_workspace.main.id
  role_definition_id = "/subscriptions/${split("/", azurerm_monitor_workspace.main.id)[2]}/providers/Microsoft.Authorization/roleDefinitions/b0d8363b-8ddd-447d-831f-62ca05bff136"
  principal_id       = azurerm_dashboard_grafana.main.identity.0.principal_id
}

resource "azurerm_role_assignment" "self_grafana" {
  scope                = azurerm_dashboard_grafana.main.id
  role_definition_name = "Grafana Admin"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_role_assignment" "aks" {
  scope                = azurerm_resource_group.main.id
  role_definition_name = "Contributor"
  principal_id         = azurerm_user_assigned_identity.main.principal_id
}