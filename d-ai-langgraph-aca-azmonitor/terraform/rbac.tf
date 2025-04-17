resource "azurerm_role_assignment" "current_user_storage_data_owner" {
  scope                = azurerm_storage_account.main.id
  role_definition_name = "Storage Blob Data Owner"
  principal_id         = data.azurerm_client_config.current.object_id
}

# resource "azurerm_role_assignment" "current_user_storage_queue_contributor" {
#   scope                = azurerm_storage_account.main.id
#   role_definition_name = "Storage Queue Data Contributor"
#   principal_id         = data.azurerm_client_config.current.object_id
# }

# resource "azurerm_role_assignment" "current_user_storage_account_contributor" {
#   scope                = azurerm_storage_account.main.id
#   role_definition_name = "Storage Account Contributor"
#   principal_id         = data.azurerm_client_config.current.object_id
# }

resource "azurerm_role_assignment" "ai_hub_storage_data_owner" {
  scope                = azurerm_storage_account.main.id
  role_definition_name = "Storage Blob Data Owner"
  principal_id         = azapi_resource.ai_hub.identity[0].principal_id
}
