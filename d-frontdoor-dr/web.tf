resource "azurerm_container_app_environment" "main" {
  name                       = random_string.main.result
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
}

resource "azurerm_container_app" "httpbin" {
  name                         = "webtester"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  template {
    container {
      name   = "webtester"
      image  = "ghcr.io/tkubica12/webtester:latest"
      cpu    = 0.25
      memory = "0.5Gi"
      env {
        name  = "APP_INSIGHTS_CONNECTION_STRING"
        value = azurerm_application_insights.main.connection_string
      }
    }
  }

  ingress {
    allow_insecure_connections = false
    target_port                = 5000
    external_enabled           = true

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}
