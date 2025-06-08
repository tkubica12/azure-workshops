resource "azurerm_role_assignment" "llm_worker_llm" {
  scope                = azurerm_resource_group.main.id
  role_definition_name = "Cognitive Services OpenAI Contributor"
  principal_id         = azapi_resource.llm_worker.output.identity.principalId
}

resource "azurerm_role_assignment" "history_worker_llm" {
  scope                = azurerm_resource_group.main.id
  role_definition_name = "Cognitive Services OpenAI User"
  principal_id         = azapi_resource.history_worker.output.identity.principalId
}

resource "azurerm_role_assignment" "memory_worker_llm" {
  scope                = azurerm_resource_group.main.id
  role_definition_name = "Cognitive Services OpenAI User"
  principal_id         = azapi_resource.memory_worker.output.identity.principalId
}

resource "azurerm_role_assignment" "memory_api_llm" {
  scope                = azurerm_resource_group.main.id
  role_definition_name = "Cognitive Services OpenAI User"
  principal_id         = azapi_resource.memory_api.output.identity.principalId
}
