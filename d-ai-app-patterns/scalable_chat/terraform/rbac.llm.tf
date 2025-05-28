resource "azurerm_role_assignment" "llm_worker_llm" {
  scope                = azurerm_resource_group.main.id
  role_definition_name = "Cognitive Services OpenAI Contributor"
  principal_id         = azapi_resource.llm_worker.output.identity.principalId
}
