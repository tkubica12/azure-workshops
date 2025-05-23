// Azure OpenAI models
resource "azurerm_cognitive_deployment" "openai_model" {
  name                 = "gpt-4.1-nano"
  cognitive_account_id = azapi_resource.ai_service.id

  model {
    format  = "OpenAI"
    name    = "gpt-4.1-nano"
    version = "2025-04-14"
  }

  sku {
    capacity = 400
    name     = "GlobalStandard"
  }
}

