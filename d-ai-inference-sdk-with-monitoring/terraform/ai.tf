resource "azapi_resource" "ai_service" {
  type      = "Microsoft.CognitiveServices/accounts@2023-10-01-preview"
  name      = "aidemo-${local.base_name}"
  location  = azurerm_resource_group.main.location
  parent_id = azurerm_resource_group.main.id

  identity {
    type = "SystemAssigned"
  }

  body = {
    name = "aidemo-${local.base_name}"
    properties = {
      #   restore             = true
      customSubDomainName = local.base_name
      apiProperties = {
        statisticsEnabled = false
      }
    }
    kind = "AIServices"
    sku = {
      name = "S0"
    }
  }
  response_export_values = ["*"]
}

resource "azapi_resource" "ai_hub" {
  type      = "Microsoft.MachineLearningServices/workspaces@2024-04-01-preview"
  name      = "aidemo-hub-${local.base_name}"
  location  = azurerm_resource_group.main.location
  parent_id = azurerm_resource_group.main.id

  identity {
    type = "SystemAssigned"
  }

  body = {
    properties = {
      description         = "This is my Azure AI hub"
      friendlyName        = "AI demo hub"
      storageAccount      = azurerm_storage_account.main.id
      keyVault            = azurerm_key_vault.main.id
      applicationInsights = azurerm_application_insights.main.id
      # containerRegistry = azurerm_container_registry.default.id
    }
    kind = "Hub"
  }

  lifecycle {
    ignore_changes = [tags]
  }
}

resource "azapi_resource" "ai_project" {
  type      = "Microsoft.MachineLearningServices/workspaces@2024-04-01-preview"
  name      = "aidemo-project-${local.base_name}"
  location  = azurerm_resource_group.main.location
  parent_id = azurerm_resource_group.main.id

  identity {
    type = "SystemAssigned"
  }

  body = {
    properties = {
      description   = "This is my Azure AI PROJECT"
      friendlyName  = "AI demo Project"
      hubResourceId = azapi_resource.ai_hub.id
    }
    kind = "Project"
  }
}

resource "azapi_resource" "ai_services_connection" {
  type      = "Microsoft.MachineLearningServices/workspaces/connections@2024-04-01-preview"
  name      = "default-${local.base_name}"
  parent_id = azapi_resource.ai_hub.id

  body = {
    properties = {
      category = "AIServices"
      target   = azapi_resource.ai_service.output.properties.endpoint
      #   target        = jsondecode(azapi_resource.AIServicesResource.output).properties.endpoint,
      authType      = "AAD"
      isSharedToAll = true
      metadata = {
        ApiType    = "Azure"
        ResourceId = azapi_resource.ai_service.id
      }
    }
  }
}

resource "azapi_resource" "model_phi35" {
  type      = "Microsoft.MachineLearningServices/workspaces/serverlessEndpoints@2024-04-01"
  name      = "phi35-${local.base_name}"
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
        modelId = "azureml://registries/azureml/models/Phi-3.5-MoE-instruct"
      }
    }
  }

  response_export_values = ["*"]
}

data "azapi_resource_action" "model_phi35_keys" {
  type                   = "Microsoft.MachineLearningServices/workspaces/serverlessEndpoints@2024-04-01"
  resource_id            = azapi_resource.model_phi35.id
  action                 = "listKeys"
  response_export_values = ["*"]
}

