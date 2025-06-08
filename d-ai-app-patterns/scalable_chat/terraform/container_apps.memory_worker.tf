resource "azapi_resource" "memory_worker" {
  type      = "Microsoft.App/containerApps@2025-01-01"
  name      = "ca-memoryworker-${local.base_name}"
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
      }
      template = {
        containers = [
          {
            name  = "memory-worker"
            image = "ghcr.io/tkubica12/azure-workshops/d-ai-app-patterns-scalable-chat-memory-worker:latest"
            resources = {
              cpu    = 0.25
              memory = "0.5Gi"
            }
            env = [
              {
                name  = "SERVICEBUS_FULLY_QUALIFIED_NAMESPACE"
                value = "${azurerm_servicebus_namespace.main.name}.servicebus.windows.net"
              },
              {
                name  = "SERVICEBUS_MESSAGE_COMPLETED_TOPIC"
                value = azurerm_servicebus_topic.message_completed.name
              },
              {
                name  = "SERVICEBUS_MESSAGE_COMPLETED_SUBSCRIPTION"
                value = azurerm_servicebus_subscription.memory_worker_message_completed.name
              },
              {
                name  = "REDIS_HOST"
                value = azapi_resource.redis.output.properties.hostName
              },
              {
                name  = "REDIS_PORT"
                value = "10000"
              },
              {
                name  = "REDIS_SSL"
                value = "true"
              },
              {
                name  = "MEMORY_API_BASE_URL"
                value = "https://${azapi_resource.memory_api.output.properties.configuration.ingress.fqdn}"
              },
              {
                name  = "AZURE_AI_CHAT_ENDPOINT"
                value = "https://${azapi_resource.ai_service.name}.cognitiveservices.azure.com/openai/deployments/${azurerm_cognitive_deployment.openai_model.name}"
              },
              {
                name  = "AZURE_AI_EMBEDDINGS_ENDPOINT"
                value = "https://${azapi_resource.ai_service.name}.cognitiveservices.azure.com/openai/deployments/${azurerm_cognitive_deployment.embedding_model.name}"
              },
              {
                name  = "MAX_CONCURRENCY"
                value = "10"
              },
              {
                name  = "LOG_LEVEL"
                value = "INFO"
              },
              {
                name  = "APPLICATIONINSIGHTS_CONNECTION_STRING"
                value = azurerm_application_insights.main.connection_string
              },
              {
                name  = "OTEL_SERVICE_NAME"
                value = "memory-worker"
              }
            ]
          }
        ]
        scale = {
          minReplicas = 0
          maxReplicas = 5
          rules = [
            {
              name = "service-bus-topic-scale-rule"
              custom = {
                type = "azure-servicebus"
                metadata = {
                  topicName        = azurerm_servicebus_topic.message_completed.name
                  subscriptionName = azurerm_servicebus_subscription.memory_worker_message_completed.name
                  namespace        = azurerm_servicebus_namespace.main.name
                  messageCount     = "5"
                },
                identity = "system"
              }
            }
          ]
        }
      }
    }
  }
}
