resource "azurerm_container_app" "front_service" {
  name                         = "ca-frontservice-${local.base_name}"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  identity {
    type = "SystemAssigned"
  }

  ingress {
    external_enabled = true
    target_port      = 8000 
    transport        = "http"

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 1
    max_replicas = 5

    container {
      name   = "front-service"
      image  = "ghcr.io/tkubica12/azure-workshops/d-ai-app-patterns-scalable-chat-front-service:latest" 
      cpu    = 0.5
      memory = "1.0Gi"

      env {
        name  = "SERVICEBUS_FULLY_QUALIFIED_NAMESPACE"
        value = "${azurerm_servicebus_namespace.main.name}.servicebus.windows.net"
      }
      env {
        name  = "SERVICEBUS_USER_MESSAGES_TOPIC"
        value = azurerm_servicebus_topic.user_messages.name
      }
      env {
        name  = "SERVICEBUS_TOKEN_STREAMS_TOPIC"
        value = azurerm_servicebus_topic.token_streams.name
      }
      env {
        name  = "SERVICEBUS_TOKEN_STREAMS_SUBSCRIPTION"
        value = azurerm_servicebus_subscription.front_service.name
      }
      env {
        name  = "SERVICEBUS_SENDER_POOL_SIZE"
        value = "10" 
      }
      env {
        name  = "LOG_LEVEL"
        value = "INFO"
      }
      env {
        name  = "CORS_ORIGINS"
        value = "*" 
      }
      env {
        name  = "APPLICATIONINSIGHTS_CONNECTION_STRING"
        value = azurerm_application_insights.main.connection_string
      }
      env {
        name  = "OTEL_SERVICE_NAME"
        value = "front-service" 
      }
    }
  }
}
