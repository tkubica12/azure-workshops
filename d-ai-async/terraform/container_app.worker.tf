resource "azurerm_container_app" "api_worker" {
  name                         = "ca-worker-${local.base_name}"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.main.id
    ]
  }

  template {
    min_replicas = 0
    max_replicas = 2

    container {
      name   = "myapp"
      image  = "ghcr.io/tkubica12/azure-workshops/d-ai-async-worker:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "APPLICATIONINSIGHTS_CONNECTION_STRING"
        value = azurerm_application_insights.main.connection_string
      }
      env {
        name  = "STORAGE_ACCOUNT_URL"
        value = azurerm_storage_account.main.primary_blob_endpoint
      }
      env {
        name  = "STORAGE_CONTAINER"
        value = azurerm_storage_container.main.name
      }
      env {
        name  = "SERVICEBUS_FQDN"
        value = azurerm_servicebus_namespace.main.endpoint
      }
      env {
        name  = "SERVICEBUS_QUEUE"
        value = azurerm_servicebus_queue.main.name
      }
      env {
        name  = "AZURE_CLIENT_ID"
        value = azurerm_user_assigned_identity.main.client_id
      }
      env {
        name  = "BATCH_SIZE"
        value = "10"
      }
      env {
        name  = "BATCH_MAX_WAIT_TIME"
        value = "1"
      }
      env {
        name  = "AZURE_OPENAI_API_KEY"
        value = var.azure_openai_api_key
      }
      env {
        name  = "AZURE_OPENAI_ENDPOINT"
        value = var.azure_openai_endpoint
      }
      env {
        name  = "AZURE_OPENAI_DEPLOYMENT_NAME"
        value = "gpt-4o"
      }
      env {
        name  = "COSMOS_ACCOUNT_URL"
        value = azurerm_cosmosdb_account.main.endpoint
      }
      env {
        name  = "COSMOS_DB_NAME"
        value = azurerm_cosmosdb_sql_database.main.name
      }
      env {
        name  = "COSMOS_CONTAINER_NAME"
        value = azurerm_cosmosdb_sql_container.main.name
      }
    }
  }
}
