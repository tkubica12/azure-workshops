resource "azurerm_container_app" "bookapp_frontend" {
  name                         = "ca-bookapp-frontend"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  ingress {
    external_enabled = true
    target_port      = 80

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.main.id]
  }

  template {
    min_replicas = 0
    max_replicas = 1

    container {
      name   = "frontend"
      image  = "ghcr.io/tkubica12/jnt-apim-hackathon/bookapp_frontend:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "REACT_APP_API_BASE_URL"
        value = "https://TBD.azure-api.net/api"    # CHANGE THIS
      }
      env {
        name  = "REACT_APP_APPLICATION_INSIGHTS_CONNECTION_STRING"
        value = azurerm_application_insights.main.connection_string
      }
    }
  }
}