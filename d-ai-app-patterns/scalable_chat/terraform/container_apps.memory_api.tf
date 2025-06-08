resource "azapi_resource" "memory_api" {
  type      = "Microsoft.App/containerApps@2025-01-01"
  name      = "ca-memoryapi-${local.base_name}"
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
          targetPort = 8003
          transport  = "http"
          allowInsecure = false
          traffic = [
            {
              weight = 100
              latestRevision = true
            }
          ]
        }
      }
      template = {
        containers = [
          {
            name  = "memory-api"
            image = "ghcr.io/tkubica12/azure-workshops/d-ai-app-patterns-scalable-chat-memory-api:latest"
            resources = {
              cpu    = 0.25
              memory = "0.5Gi"
            }
            env = [
              {
                name  = "COSMOS_ENDPOINT"
                value = azurerm_cosmosdb_account.main.endpoint
              },
              {
                name  = "COSMOS_DATABASE_NAME"
                value = azurerm_cosmosdb_sql_database.memory.name
              },
              {
                name  = "COSMOS_CONVERSATIONS_CONTAINER_NAME"
                value = azapi_resource.memory_conversations.name
              },
              {
                name  = "COSMOS_USER_MEMORIES_CONTAINER_NAME"
                value = azapi_resource.memory_user_memories.name
              },
              {
                name  = "AZURE_AI_EMBEDDINGS_ENDPOINT"
                value = "https://${azapi_resource.ai_service.name}.cognitiveservices.azure.com/openai/deployments/${azurerm_cognitive_deployment.embedding_model.name}"
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
                name  = "PORT"
                value = "8003"
              },
              {
                name  = "APPLICATIONINSIGHTS_CONNECTION_STRING"
                value = azurerm_application_insights.main.connection_string
              },
              {
                name  = "OTEL_SERVICE_NAME"
                value = "memory-api"
              }
            ]
          }
        ]
        scale = {
          minReplicas = 0
          maxReplicas = 5
          rules = [
            {
              name = "http-scale-rule"
              http = {
                metadata = {
                  concurrentRequests = "10"
                }
              }
            }
          ]
        }
      }
    }
  }
}
