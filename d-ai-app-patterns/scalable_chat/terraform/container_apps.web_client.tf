resource "azurerm_container_app" "web_client" {
  name                         = "ca-webclient-${local.base_name}"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  ingress {
    external_enabled = true
    target_port      = 80 
    transport        = "http" 

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 0
    max_replicas = 1 // Adjust as needed

    container {
      name   = "web-client"
      image  = "ghcr.io/tkubica12/azure-workshops/d-ai-app-patterns-scalable-chat-web-client:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "API_URL"
        value = "https://${azurerm_container_app.front_service.ingress[0].fqdn}"
      }
    }
  }
}
