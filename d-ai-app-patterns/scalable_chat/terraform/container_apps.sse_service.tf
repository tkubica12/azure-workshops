resource "azapi_resource" "sse_service" {
  type      = "Microsoft.App/containerApps@2025-01-01"
  name      = "ca-sseservice-${local.base_name}"
  location  = azurerm_resource_group.main.location
  parent_id = azurerm_resource_group.main.id

  body = {
    identity = {
      type = "SystemAssigned"
    }
    properties = {
      managedEnvironmentId = azurerm_container_app_environment.main.id
      configuration = {
        activeRevisionsMode = "Single"
        ingress = {
          external   = true
          targetPort = 8002
          transport  = "Http"
          traffic = [
            {
              latestRevision = true
              weight         = 100
            }
          ]
        }
      }
      template = {
        scale = {
          minReplicas = 0
          maxReplicas = 10
          rules = [
            {
              name = "http-scale-rule"
              http = {
                metadata = {
                  concurrentRequests = "20"
                }
              }
            }
          ]
        }
        containers = [
          {
            name  = "sse-service"
            image = "ghcr.io/tkubica12/azure-workshops/d-ai-app-patterns-scalable-chat-sse-service:latest"
            resources = {
              cpu    = 0.5
              memory = "1Gi"
            }
            env = [
              {
                name  = "SERVICEBUS_FULLY_QUALIFIED_NAMESPACE"
                value = "${azurerm_servicebus_namespace.main.name}.servicebus.windows.net"
              },
              {
                name  = "SERVICEBUS_TOKEN_STREAMS_TOPIC"
                value = azurerm_servicebus_topic.token_streams.name
              },
              {
                name  = "SERVICEBUS_TOKEN_STREAMS_SUBSCRIPTION"
                value = azurerm_servicebus_subscription.front_service_token_streams.name
              },
              {
                name  = "LOG_LEVEL"
                value = "INFO"
              },
              {
                name  = "CORS_ORIGINS"
                value = "*"
              },
              {
                name  = "APPLICATIONINSIGHTS_CONNECTION_STRING"
                value = azurerm_application_insights.main.connection_string
              },
              {
                name  = "OTEL_SERVICE_NAME"
                value = "sse-service"
              }
            ]
          }
        ]
      }
    }
  }
}
