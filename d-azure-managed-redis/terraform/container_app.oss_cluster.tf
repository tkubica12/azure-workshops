resource "azurerm_container_app" "oss_cluster" {
  name                         = "ca-oss-cluster"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  template {
    container {
      name   = "myapp"
      image  = "ghcr.io/tkubica12/azure-workshops/d-azure-managed-redis-test:latest"
      cpu    = 2
      memory = "4Gi"

      env {
        name  = "REDIS_CLUSTER_MODE"
        value = "oss"
      }

      env {
        name  = "REDIS_OSS_HOST"
        value = azapi_resource.redis_clusteross.output.properties.hostName
      }

      env {
        name  = "REDIS_ENTERPRISE_HOST"
        value = azapi_resource.redis_clusterenterprise.output.properties.hostName
      }

      env {
        name  = "REDIS_GEO_PRIMARY_HOST"
        value = azapi_resource.redis_geo1.output.properties.hostName
      }

      env {
        name  = "REDIS_PORT"
        value = 10000
      }

      env {
        name  = "AZURE_OPENAI_ENDPOINT"
        value = azurerm_cognitive_account.openai.endpoint
      }

      env {
        name  = "AZURE_OPENAI_EMBEDDINGS_MODEL"
        value = azurerm_cognitive_deployment.text-embedding-3-large.model[0].name
      }

      env {
        name  = "AZURE_CLIENT_ID"
        value = azurerm_user_assigned_identity.app.client_id
      }
    }
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.app.id]
  }
}
