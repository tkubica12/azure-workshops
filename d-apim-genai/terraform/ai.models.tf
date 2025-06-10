resource "azurerm_cognitive_deployment" "openai_model_p1" {
  name                 = "gpt-4.1"
  cognitive_account_id = azapi_resource.ai_service_p1.id
  model {
    format  = "OpenAI"
    name    = "gpt-4.1"
    version = "2025-04-14"
  }

  sku {
    capacity = 5
    name     = "GlobalStandard"
  }

  depends_on = [data.azapi_resource_action.openai_model_key_p1]
}

resource "azurerm_cognitive_deployment" "openai_model_p2" {
  name                 = "gpt-4.1"
  cognitive_account_id = azapi_resource.ai_service_p2.id
  model {
    format  = "OpenAI"
    name    = "gpt-4.1"
    version = "2025-04-14"
  }

  sku {
    capacity = 10
    name     = "GlobalStandard"
  }

  depends_on = [data.azapi_resource_action.openai_model_key_p2]
}

resource "azurerm_cognitive_deployment" "embeddings" {
  name                 = "text-embedding-3-large"
  cognitive_account_id = azapi_resource.ai_service_p1.id
  model {
    format  = "OpenAI"
    name    = "text-embedding-3-large"
    version = "1"
  }

  sku {
    capacity = 50
    name     = "Standard"
  }

  depends_on = [data.azapi_resource_action.openai_model_key_p1]
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

