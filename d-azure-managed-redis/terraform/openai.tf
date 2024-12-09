resource "azurerm_cognitive_account" "openai" {
  name                  = "openai-${local.base_name}"
  location              = azurerm_resource_group.main.location
  resource_group_name   = azurerm_resource_group.main.name
  kind                  = "OpenAI"
  sku_name              = "S0"
  custom_subdomain_name = "openai-${local.base_name}"
}


resource "azurerm_cognitive_deployment" "text-embedding-3-large" {
  name                 = "text-embedding-3-large"
  cognitive_account_id = azurerm_cognitive_account.openai.id

  model {
    format  = "OpenAI"
    name    = "text-embedding-3-large"
    version = "1"
  }

  sku {
    name     = "Standard"
    capacity = 2
  }
}

resource "azurerm_role_assignment" "openai_app" {
  scope                = azurerm_cognitive_account.openai.id
  role_definition_name = "Cognitive Services OpenAI User"
  principal_id         = azurerm_user_assigned_identity.app.principal_id
}

resource "azurerm_role_assignment" "openai_self" {
  scope                = azurerm_cognitive_account.openai.id
  role_definition_name = "Cognitive Services OpenAI Contributor"
  principal_id         = data.azurerm_client_config.current.object_id
}
