resource "azapi_resource" "redis_clusterenterprise" {
  type                      = "Microsoft.Cache/redisEnterprise@2024-09-01-preview"
  name                      = "redis-clusterenterprise-${local.base_name}"
  parent_id                 = azurerm_resource_group.main.id
  location                  = azurerm_resource_group.main.location
  schema_validation_enabled = false
  body = {
    sku = {
      name = "ComputeOptimized_X3"
    }
    properties = {
      highAvailability = "Disabled"
    }
  }
}

resource "azapi_resource" "redis_clusterenteprise_database" {
  type      = "Microsoft.Cache/redisEnterprise/databases@2024-09-01-preview"
  name      = "default"
  parent_id = azapi_resource.redis_clusterenterprise.id
  body = {
    properties = {
      clientProtocol   = "Encrypted"
      evictionPolicy   = "NoEviction"
      clusteringPolicy = "EnterpriseCluster" # OSSCluster or EnterpriseCluster
      deferUpgrade     = "NotDeferred"
      modules = [
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

data "azapi_resource_action" "redis_database_list_keys" {
  type                   = "Microsoft.Cache/redisEnterprise/databases@2024-09-01-preview"
  action                 = "listKeys"
  resource_id            = azapi_resource.redis_clusterenteprise_database.id
  method                 = "POST"
  response_export_values = ["*"]
}

locals {
  redis_connection_string = "${azapi_resource.redis_clusterenterprise.output.properties.hostName}:10000,password=${data.azapi_resource_action.redis_database_list_keys.output.primaryKey},ssl=True,abortConnect=False"
}

resource "azapi_resource" "redis_clusterenteprise_access_self" {
  type      = "Microsoft.Cache/redisEnterprise/databases/accessPolicyAssignments@2024-09-01-preview"
  name      = "self"
  parent_id = azapi_resource.redis_clusterenteprise_database.id
  body = {
    properties = {
      accessPolicyName = "default"
      user = {
        objectId = data.azurerm_client_config.current.object_id
      }
    }
  }
}

resource "azapi_resource" "redis_clusterenteprise_access_apim" {
  type      = "Microsoft.Cache/redisEnterprise/databases/accessPolicyAssignments@2024-09-01-preview"
  name      = "apim"
  parent_id = azapi_resource.redis_clusterenteprise_database.id
  body = {
    properties = {
      accessPolicyName = "default"
      user = {
        objectId = azurerm_api_management.main.identity.0.principal_id
      }
    }
  }
}

