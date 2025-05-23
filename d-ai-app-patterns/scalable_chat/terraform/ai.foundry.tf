resource "azapi_resource" "ai_service" {
  type      = "Microsoft.CognitiveServices/accounts@2023-10-01-preview"
  name      = "aidemo-${local.base_name}"
  location  = var.llm_location
  parent_id = azurerm_resource_group.main.id

  identity {
    type = "SystemAssigned"
  }

  body = {
    name = "aidemo-${local.base_name}"
    properties = {
        # restore             = true
      customSubDomainName = "aidemo-${local.base_name}"
      #   apiProperties = {
      #     statisticsEnabled = false
      #   }
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
  location  = var.llm_location
  parent_id = azurerm_resource_group.main.id

  identity {
    type = "SystemAssigned"
  }

  body = {
    properties = {
      description         = "This is my Azure AI hub"
      friendlyName        = "AI demo hub"
      storageAccount      = azapi_resource.storage_account_main.id
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
  location  = var.llm_location
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
      category      = "AIServices"
      target        = azapi_resource.ai_service.output.properties.endpoint
      authType      = "AAD"
      isSharedToAll = true
      metadata = {
        ApiType    = "Azure"
        ResourceId = azapi_resource.ai_service.id
      }
    }
  }
}



