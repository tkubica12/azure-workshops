resource "azapi_resource" "redis_access_self" {
  type      = "Microsoft.Cache/redisEnterprise/databases/accessPolicyAssignments@2024-09-01-preview"
  name      = "self"
  parent_id = azapi_resource.redis_db.id
  body = {
    properties = {
      accessPolicyName = "default"
      user = {
        objectId = data.azurerm_client_config.current.object_id
      }
    }
  }
}

resource "azapi_resource" "redis_access_history_worker" {
  type      = "Microsoft.Cache/redisEnterprise/databases/accessPolicyAssignments@2024-09-01-preview"
  name      = "historyworker"
  parent_id = azapi_resource.redis_db.id
  body = {
    properties = {
      accessPolicyName = "default"
      user = {
        objectId = azapi_resource.history_worker.output.identity.principalId
      }
    }
  }
}

resource "azapi_resource" "redis_access_memory_worker" {
  type      = "Microsoft.Cache/redisEnterprise/databases/accessPolicyAssignments@2024-09-01-preview"
  name      = "memoryworker"
  parent_id = azapi_resource.redis_db.id
  body = {
    properties = {
      accessPolicyName = "default"
      user = {
        objectId = azapi_resource.memory_worker.output.identity.principalId
      }
    }
  }
}