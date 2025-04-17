locals {
  serverless_models = {
    # "phi35-MoE" = {
    #   model_id = "azureml://registries/azureml/models/Phi-3.5-MoE-instruct"
    # }
    # "phi35-mini" = {
    #   model_id = "azureml://registries/azureml/models/Phi-3.5-mini-instruct"
    # }
    # "mixtral-8x22B" = "azureml://registries/azureml/models/mistralai-Mixtral-8x22B-Instruct-v0-1"
    # "mixtral-8x7B" = "azureml://registries/azureml/models/mistralai-Mixtral-8x7B-Instruct-v01"
    # "mistral-7B" = "azureml://registries/azureml/models/mistralai-Mistral-7B-v01"
    # "phi4" = "azureml://registries/azureml/models/Phi-4"
  }
  openai_models = {
    "gpt-4.1-mini" = {
      model_id     = "gpt-4.1-mini"
      version      = "2025-04-14"
      sku_name     = "GlobalStandard"
      sku_capacity = 100
    }
    "gpt-4.1-nano" = {
      model_id     = "gpt-4.1-nano"
      version      = "2025-04-14"
      sku_name     = "GlobalStandard"
      sku_capacity = 100
    }
    "gpt-4.1" = {
      model_id     = "gpt-4.1-mini"
      version      = "2025-04-14"
      sku_name     = "GlobalStandard"
      sku_capacity = 100
    }
  }
}
// Serverless models
resource "azapi_resource" "serverless_model" {
  for_each  = local.serverless_models
  type      = "Microsoft.MachineLearningServices/workspaces/serverlessEndpoints@2024-04-01"
  name      = "${each.key}-${local.base_name}"
  parent_id = azapi_resource.ai_project.id
  location  = azurerm_resource_group.main.location

  body = {
    sku = {
      name = "Consumption"
    }
    properties = {
      authMode = "Key"
      contentSafety = {
        contentSafetyStatus = "Enabled"
      }
      modelSettings = {
        modelId = each.value.model_id
      }
    }
  }

  response_export_values = ["*"]
}

data "azapi_resource_action" "serverless_model_key" {
  for_each               = azapi_resource.serverless_model
  type                   = "Microsoft.MachineLearningServices/workspaces/serverlessEndpoints@2024-04-01"
  resource_id            = each.value.id
  action                 = "listKeys"
  response_export_values = ["*"]
}

// Azure OpenAI models
resource "azurerm_cognitive_deployment" "openai_model" {
  for_each             = local.openai_models
  name                 = each.key
  cognitive_account_id = azapi_resource.ai_service.id
  model {
    format  = "OpenAI"
    name    = each.value.model_id
    version = each.value.version
  }

  sku {
    capacity = each.value.sku_capacity
    name     = each.value.sku_name
  }

  depends_on = [data.azapi_resource_action.openai_model_key]
}

data "azapi_resource_action" "openai_model_key" {
  type                   = "Microsoft.CognitiveServices/accounts@2023-05-01"
  resource_id            = azapi_resource.ai_service.id
  action                 = "listKeys"
  response_export_values = ["*"]
}

// Prepare config
locals {
  model_configurations = {
    models = merge(
      {
        for model_name, model in local.serverless_models :
        model_name => {
          endpoint = azapi_resource.serverless_model[model_name].output.properties.inferenceEndpoint.uri
          key      = data.azapi_resource_action.serverless_model_key[model_name].output.primaryKey
        }
      },
      {
        for model_name, model in local.openai_models :
        model_name => {
          endpoint = "${azapi_resource.ai_service.output.properties.endpoints["Azure AI Model Inference API"]}/openai/deployments/${model_name}"
          key      = data.azapi_resource_action.openai_model_key.output.key1
        }
      }
    )
  }
}

output "model_configurations" {
  value = jsonencode(local.model_configurations)
}
