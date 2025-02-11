resource "azurerm_api_management_product" "gold" {
  product_id            = "gold"
  api_management_name   = azurerm_api_management.main.name
  resource_group_name   = azurerm_resource_group.main.name
  display_name          = "Gold tier"
  description           = "Gold tier subscription includes unlimited access to the OpenAI API."
  subscription_required = true
  approval_required     = false
  published             = true
}


resource "azurerm_api_management_product" "silver" {
  product_id            = "silver"
  api_management_name   = azurerm_api_management.main.name
  resource_group_name   = azurerm_resource_group.main.name
  display_name          = "Silver tier"
  description           = "Silver tier subscription includes 1000 tokens per minute to the OpenAI API."
  subscription_required = true
  approval_required     = false
  published             = true
}

resource "azurerm_api_management_product" "caching" {
  product_id            = "caching"
  api_management_name   = azurerm_api_management.main.name
  resource_group_name   = azurerm_resource_group.main.name
  display_name          = "Caching tier"
  description           = "Caching tier subscription includes caching capabilities for the OpenAI API."
  subscription_required = true
  approval_required     = false
  published             = true
}

resource "azurerm_api_management_product_api" "gold" {
  product_id          = azurerm_api_management_product.gold.product_id
  api_name            = azurerm_api_management_api.openai.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_api_management_product_api" "silver" {
  product_id          = azurerm_api_management_product.silver.product_id
  api_name            = azurerm_api_management_api.openai.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_api_management_product_api" "caching" {
  product_id          = azurerm_api_management_product.caching.product_id
  api_name            = azurerm_api_management_api.openai.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
}
