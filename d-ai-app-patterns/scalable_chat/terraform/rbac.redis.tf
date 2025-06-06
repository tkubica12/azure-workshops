
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


# resource "azapi_resource" "redis_access_app" {
#   type      = "Microsoft.Cache/redisEnterprise/databases/accessPolicyAssignments@2024-09-01-preview"
#   name      = "app"
#   parent_id = azapi_resource.redis.id
#   body = {
#     properties = {
#       accessPolicyName = "default"
#       user = {
#         objectId = azurerm_user_assigned_identity.app.principal_id
#       }
#     }
#   }
# }