resource "azurerm_cognitive_deployment" "openai_model_p1" {
  name                 = "gpt-4o-mini-p1"
  cognitive_account_id = azapi_resource.ai_service.id
  model {
    format  = "OpenAI"
    name    = "gpt-4o-mini"
    version = "2024-07-18"
  }

  sku {
    capacity = 5
    name     = "GlobalStandard"
  }

  depends_on = [data.azapi_resource_action.openai_model_key]
}

resource "azurerm_cognitive_deployment" "openai_model_p2" {
  name                 = "gpt-4o-mini-p2"
  cognitive_account_id = azapi_resource.ai_service.id
  model {
    format  = "OpenAI"
    name    = "gpt-4o-mini"
    version = "2024-07-18"
  }

  sku {
    capacity = 10
    name     = "GlobalStandard"
  }

  depends_on = [data.azapi_resource_action.openai_model_key]
}

data "azapi_resource_action" "openai_model_key" {
  type                   = "Microsoft.CognitiveServices/accounts@2023-05-01"
  resource_id            = azapi_resource.ai_service.id
  action                 = "listKeys"
  response_export_values = ["*"]
}

