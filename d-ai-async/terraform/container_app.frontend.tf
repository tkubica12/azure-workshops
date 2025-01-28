resource "azurerm_container_app" "api_frontend" {
  name                         = "ca-frontend-${local.base_name}"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.main.id
    ]
  }

  ingress {
    external_enabled = true
    target_port      = 80

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 0
    max_replicas = 2

    container {
      name   = "myapp"
      image  = "ghcr.io/tkubica12/azure-workshops/d-ai-async-frontend:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "APPLICATIONINSIGHTS_CONNECTION_STRING"
        value = azurerm_application_insights.main.connection_string
      }
      env {
        name  = "REACT_APP_PROCESS_API_URL"
        value = "https://${azurerm_container_app.api_processing.ingress[0].fqdn}/api/status"
      }
    }
  }
}
