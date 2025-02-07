resource "azurerm_role_assignment" "apim_to_aimodel_p1" {
  principal_id         = azurerm_user_assigned_identity.main.principal_id
  role_definition_name = "Cognitive Services OpenAI User"
  scope                = azapi_resource.ai_service_p1.id
}

resource "azurerm_role_assignment" "apim_to_aimodel_p2" {
  principal_id         = azurerm_user_assigned_identity.main.principal_id
  role_definition_name = "Cognitive Services OpenAI User"
  scope                = azapi_resource.ai_service_p2.id
}
