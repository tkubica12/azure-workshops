resource "azapi_resource" "redis" {
  type                      = "Microsoft.Cache/redisEnterprise@2025-05-01-preview"
  name                      = "redis-${local.base_name}"
  parent_id                 = azurerm_resource_group.main.id
  location                  = azurerm_resource_group.main.location
  schema_validation_enabled = true
  body = {
    sku = {
      name = "Balanced_B1"
    }
    properties = {
      highAvailability = "Enabled"
    }
  }
}
resource "azapi_resource" "redis_db" {
  type      = "Microsoft.Cache/redisEnterprise/databases@2025-05-01-preview"
  name      = "default"
  parent_id = azapi_resource.redis.id
  body = {
    properties = {
      clientProtocol           = "Encrypted"
      evictionPolicy           = "NoEviction"
      clusteringPolicy         = "EnterpriseCluster"
      deferUpgrade             = "NotDeferred"
      accessKeysAuthentication = "Disabled"
      modules = [
        {
          name = "RedisJSON"
        }
      ]
      persistence = {
        aofEnabled   = true
        aofFrequency = "1s"
        rdbEnabled   = false
      }
    }
  }
}


