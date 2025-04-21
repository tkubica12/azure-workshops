resource "azurerm_container_app" "gradio" {
  name                         = "ca-multiagent-${local.base_name}"
  container_app_environment_id = azapi_resource.capp_env.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  ingress {
    external_enabled = true
    target_port      = 8501

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
      image  = "ghcr.io/tkubica12/azure-workshops/d-ai-langgraph-multiagent:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "AZURE_OPENAI_ENDPOINT"
        value = local.model_configurations.models["gpt-4.1"].endpoint
      }

      env {
        name  = "AZURE_OPENAI_API_KEY"
        value = local.model_configurations.models["gpt-4.1"].key
      }

      env {
        name  = "APPLICATIONINSIGHTS_CONNECTION_STRING"
        value = azurerm_application_insights.main.connection_string
      }

      env {
        name  = "OTEL_TRACES_EXPORTER"
        value = "console,otlp"
      }

      env {
        name  = "OTEL_SERVICE_NAME"
        value = "my-multiagent-ai"
      }

      env {
        name  = "AZURE_OPENAI_DEPLOYMENT_NAME"
        value = "gpt-4.1"
      }
    }
  }
}
