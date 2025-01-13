resource "azurerm_container_app" "gradio" {
  name                         = "ca-gradio-${local.base_name}"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  ingress {
    external_enabled = true
    target_port      = 7860

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
      image  = "ghcr.io/tkubica12/azure-workshops/d-ai-inference-sdk-with-monitoring:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "MODELS_CONFIG"
        value = base64encode(jsonencode(local.model_configurations))
      }

      env {
        name  = "AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED"
        value = "true"
      }

      env {
        name  = "APPLICATIONINSIGHTS_CONNECTION_STRING"
        value = azurerm_application_insights.main.connection_string
      }
    }
  }
}
