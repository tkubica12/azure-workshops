resource "azurerm_container_app" "auth_open_api" {
  name                         = "ca-auth-open-api"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  ingress {
    external_enabled = true
    target_port      = 5001

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 0
    max_replicas = 1

    container {
      name   = "myapp"
      image  = "ghcr.io/tkubica12/jnt-apim-hackathon/auth_open_api:latest"
      cpu    = 0.25
      memory = "0.5Gi"
    }
  }
}
