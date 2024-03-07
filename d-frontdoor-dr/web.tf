resource "azurerm_container_app_environment" "main" {
  name                       = random_string.main.result
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
}

resource "azurerm_container_app" "httpbin" {
  name                         = "httpbin"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  template {
    container {
      name   = "httpbin"
      image  = "kennethreitz/httpbin:latest"
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }

  ingress {
    allow_insecure_connections = false
    target_port                = 80
    external_enabled           = true

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}
