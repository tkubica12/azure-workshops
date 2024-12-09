resource "azapi_resource" "redis_geo1" {
  type                      = "Microsoft.Cache/redisEnterprise@2024-09-01-preview"
  name                      = "redis-geo1-${local.base_name}"
  parent_id                 = azurerm_resource_group.main.id
  location                  = azurerm_resource_group.main.location
  schema_validation_enabled = false
  body = {
    sku = {
      name = "ComputeOptimized_X10"
    }
    properties = {
      highAvailability = "Enabled"
    }
  }
}

resource "azapi_resource" "redis_geo2" {
  type                      = "Microsoft.Cache/redisEnterprise@2024-09-01-preview"
  name                      = "redis-geo2-${local.base_name}"
  parent_id                 = azurerm_resource_group.main.id
  location                  = var.secondary_locationazurerm_resource_group.main.location
  schema_validation_enabled = false
  body = {
    sku = {
      name = "ComputeOptimized_X10"
    }
    properties = {
      highAvailability = "Enabled"
    }
  }
}

resource "azapi_resource" "redis_geo1_database" {
  type      = "Microsoft.Cache/redisEnterprise/databases@2024-09-01-preview"
  name      = "default"
  parent_id = azapi_resource.redis_geo1.id
  body = {
    properties = {
      clientProtocol   = "Encrypted"
      evictionPolicy   = "NoEviction"
      clusteringPolicy = "EnterpriseCluster" # OSSCluster or EnterpriseCluster
      deferUpgrade     = "NotDeferred"
      geoReplication = {
        groupNickname = "mygeogroup"
        linkedDatabases = [
          {
            id = "${azapi_resource.redis_geo1.id}/databases/default"
          },
          {
            id = "${azapi_resource.redis_geo2.id}/databases/default"
          }
        ]
      }
      modules = [
        {
          name = "RedisJSON"
        },
        {
          name = "RediSearch"
        }
      ]
      persistence = {
        aofEnabled = false
        rdbEnabled = false
      }
      accessKeysAuthentication = "Enabled"
    }
  }
}

resource "azapi_resource" "redis_geo2_database" {
  type      = "Microsoft.Cache/redisEnterprise/databases@2024-09-01-preview"
  name      = "default"
  parent_id = azapi_resource.redis_geo2.id
  body = {
    properties = {
      clientProtocol   = "Encrypted"
      evictionPolicy   = "NoEviction"
      clusteringPolicy = "EnterpriseCluster" # OSSCluster or EnterpriseCluster
      deferUpgrade     = "NotDeferred"
      geoReplication = {
        groupNickname = "mygeogroup"
        linkedDatabases = [
          {
            id = "${azapi_resource.redis_geo1.id}/databases/default"
          },
          {
            id = "${azapi_resource.redis_geo2.id}/databases/default"
          }
        ]
      }
      modules = [
        {
          name = "RedisJSON"
        },
        {
          name = "RediSearch"
        }
      ]
      persistence = {
        aofEnabled = false
        rdbEnabled = false
      }
      accessKeysAuthentication = "Enabled"
    }
  }
}

resource "azapi_resource" "redis_geo1_access_self" {
  type      = "Microsoft.Cache/redisEnterprise/databases/accessPolicyAssignments@2024-09-01-preview"
  name      = "self"
  parent_id = azapi_resource.redis_geo1_database.id
  body = {
    properties = {
      accessPolicyName = "default"
      user = {
        objectId = data.azurerm_client_config.current.object_id
      }
    }
  }
}

resource "azapi_resource" "redis_geo2_access_self" {
  type      = "Microsoft.Cache/redisEnterprise/databases/accessPolicyAssignments@2024-09-01-preview"
  name      = "self"
  parent_id = azapi_resource.redis_geo2_database.id
  body = {
    properties = {
      accessPolicyName = "default"
      user = {
        objectId = data.azurerm_client_config.current.object_id
      }
    }
  }
}

resource "azapi_resource" "redis_geo1_access_app" {
  type      = "Microsoft.Cache/redisEnterprise/databases/accessPolicyAssignments@2024-09-01-preview"
  name      = "app"
  parent_id = azapi_resource.redis_geo1_database.id
  body = {
    properties = {
      accessPolicyName = "default"
      user = {
        objectId = azurerm_user_assigned_identity.app.principal_id
      }
    }
  }
}

resource "azapi_resource" "redis_geo2_access_app" {
  type      = "Microsoft.Cache/redisEnterprise/databases/accessPolicyAssignments@2024-09-01-preview"
  name      = "app"
  parent_id = azapi_resource.redis_geo2_database.id
  body = {
    properties = {
      accessPolicyName = "default"
      user = {
        objectId = azurerm_user_assigned_identity.app.principal_id
      }
    }
  }
}
