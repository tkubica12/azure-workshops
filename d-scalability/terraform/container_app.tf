resource "azurerm_log_analytics_workspace" "main" {
  name                = random_string.main.result
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "main" {
  name                       = "capp-environment"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
}

resource "azurerm_container_app" "canary" {
  name                         = "canary-app"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Multiple"

  template {

    container {
      name   = "app"
      image  = "argoproj/rollouts-demo:blue"
      cpu    = 0.25
      memory = "0.5Gi"
    }

    revision_suffix = "blue"
  }

  ingress {
    allow_insecure_connections = true
    external_enabled           = true
    target_port                = 8080

    traffic_weight {
      label           = "blue"
      revision_suffix = "blue"
      percentage      = 100
    }
  }
}
