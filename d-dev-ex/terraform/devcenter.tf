resource "azapi_resource" "dev_center" {
  type      = "Microsoft.DevCenter/devcenters@2023-04-01"
  name      = local.dev_center
  location  = azurerm_resource_group.main.location
  parent_id = azurerm_resource_group.main.id

  identity {
    type = "SystemAssigned"
  }

  body = jsonencode({
    properties = {}
  })
}

resource "azapi_resource" "dev_project" {
  type      = "Microsoft.DevCenter/projects@2023-04-01"
  name      = local.dev_project
  location  = azurerm_resource_group.main.location
  parent_id = azurerm_resource_group.main.id

  body = jsonencode({
    properties = {
      description        = "This is demo project"
      devCenterId        = azapi_resource.dev_center.id
      maxDevBoxesPerUser = 1
    }
  })
}

resource "azurerm_role_assignment" "deployment_identity" {
  scope                = "/subscriptions/${data.azurerm_client_config.current.subscription_id}"
  role_definition_name = "Owner"
  principal_id         = azapi_resource.dev_center.identity[0].principal_id
}

resource "azurerm_log_analytics_workspace" "main" {
  name                = module.base_naming.log_analytics_workspace.name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_monitor_diagnostic_setting" "main" {
  name                       = "logs"
  target_resource_id         = azapi_resource.dev_center.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id

  enabled_log {
    category_group = "allLogs"
  }

  metric {
    category = "AllMetrics"
    enabled  = "false"
  }
}
