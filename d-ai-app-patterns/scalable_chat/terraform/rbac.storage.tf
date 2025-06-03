# resource "azurerm_role_assignment" "self_storage" {
#   scope                = azurerm_storage_account.main.id
#   role_definition_name = "Storage Blob Data Owner"
#   principal_id         = data.azurerm_client_config.current.object_id
# }

# resource "azurerm_role_assignment" "app_storage" {
#   scope                = azurerm_storage_account.main.id
#   role_definition_name = "Storage Blob Data Contributor"
#   principal_id         = azurerm_user_assigned_identity.main.principal_id
# }