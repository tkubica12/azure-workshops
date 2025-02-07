resource "azurerm_cognitive_deployment" "openai_model_p1" {
  name                 = "gpt-4o-mini"
  cognitive_account_id = azapi_resource.ai_service_p1.id
  model {
    format  = "OpenAI"
    name    = "gpt-4o-mini"
    version = "2024-07-18"
  }

  sku {
    capacity = 5
    name     = "GlobalStandard"
  }

  depends_on = [data.azapi_resource_action.openai_model_key_p1]
}

resource "azurerm_cognitive_deployment" "openai_model_p2" {
  name                 = "gpt-4o-mini"
  cognitive_account_id = azapi_resource.ai_service_p2.id
  model {
    format  = "OpenAI"
    name    = "gpt-4o-mini"
    version = "2024-07-18"
  }

  sku {
    capacity = 10
    name     = "GlobalStandard"
  }

  depends_on = [data.azapi_resource_action.openai_model_key_p2]
}

data "azapi_resource_action" "openai_model_key_p1" {
  type                   = "Microsoft.CognitiveServices/accounts@2023-05-01"
  resource_id            = azapi_resource.ai_service_p1.id
  action                 = "listKeys"
  response_export_values = ["*"]
}

data "azapi_resource_action" "openai_model_key_p2" {
  type                   = "Microsoft.CognitiveServices/accounts@2023-05-01"
  resource_id            = azapi_resource.ai_service_p2.id
  action                 = "listKeys"
  response_export_values = ["*"]
}

