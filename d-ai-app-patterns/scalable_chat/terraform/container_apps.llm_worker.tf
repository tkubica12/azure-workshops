resource "azapi_resource" "llm_worker" {
  type      = "Microsoft.App/containerApps@2025-01-01"
  name      = "ca-llmworker-${local.base_name}"
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
            name  = "llm-worker"
            image = "ghcr.io/tkubica12/azure-workshops/d-ai-app-patterns-scalable-chat-llm-worker:latest"
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
                name  = "SERVICEBUS_USER_MESSAGES_TOPIC"
                value = azurerm_servicebus_topic.user_messages.name
              },
                  {
                    name  = "SERVICEBUS_USER_MESSAGES_SUBSCRIPTION"
                    value = azurerm_servicebus_subscription.worker_service_user_messages.name
                  },
              {
                name  = "SERVICEBUS_TOKEN_STREAMS_TOPIC"
                value = azurerm_servicebus_topic.token_streams.name
              },
              {
                name  = "SERVICEBUS_MESSAGE_COMPLETED_TOPIC"
                value = azurerm_servicebus_topic.message_completed.name
              },
              {
                name  = "MAX_CONCURRENCY"
                value = "100"
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
                value = "llm-worker"
              },
              {
                name  = "AZURE_AI_CHAT_ENDPOINT"
                value = "https://${azapi_resource.ai_service.name}.cognitiveservices.azure.com/openai/deployments/${azurerm_cognitive_deployment.openai_model.name}"
              }            ]
          }
        ]
        scale = {
          minReplicas = 0
          maxReplicas = 10
          rules = [
            {
              name = "service-bus-topic-scale-rule"
              custom = {
                type = "azure-servicebus"
                metadata = {
                  topicName        = azurerm_servicebus_topic.user_messages.name
                  subscriptionName = azurerm_servicebus_subscription.worker_service_user_messages.name
                  namespace        = azurerm_servicebus_namespace.main.name
                  messageCount     = "10"
                },
                identity = "system"
              }
            }
          ]
        }
        # Configure graceful shutdown with 4-minute grace period for LLM processing
        terminationGracePeriodSeconds = 240
      }
    }
  }
}
