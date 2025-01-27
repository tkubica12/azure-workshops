resource "azurerm_container_app" "api_status" {
  name                         = "ca-api-status-${local.base_name}"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.main.id
    ]
  }

  ingress {
    external_enabled = true
    target_port      = 80

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 0
    max_replicas = 2

    container {
      name   = "myapp"
      image  = "ghcr.io/tkubica12/azure-workshops/d-ai-async-api-status:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "APPLICATIONINSIGHTS_CONNECTION_STRING"
        value = azurerm_application_insights.main.connection_string
      }
      env {
        name  = "CORS_ORIGIN"
        value = "http://localhost:3000"
      }
      env {
        name  = "AZURE_CLIENT_ID"
        value = azurerm_user_assigned_identity.main.client_id
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
      env {
        name  = "RETRY_AFTER"
        value = "1"
      }
    }
  }
}
