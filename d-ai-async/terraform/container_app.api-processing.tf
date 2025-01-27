resource "azurerm_container_app" "api_processing" {
  name                         = "ca-api-processing-${local.base_name}"
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
      image  = "ghcr.io/tkubica12/azure-workshops/d-ai-async-api-processing:latest"
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
        name  = "STORAGE_ACCOUNT_URL"
        value = azurerm_storage_account.main.primary_blob_endpoint
      }
      env {
        name  = "STORAGE_CONTAINER"
        value = azurerm_storage_container.main.name
      }
      env {
        name  = "PROCESSED_BASE_URL"
        value = "https://${azurerm_container_app.api_status.ingress[0].fqdn}/api/status"
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
    }
  }
}
