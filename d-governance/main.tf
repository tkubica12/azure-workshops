resource "azurerm_resource_group" "main" {
  name     = "demo-rg"
  location = var.location
}

resource "random_string" "main" {
  length  = 16
  special = false
  numeric = false
  upper   = false
  lower   = true
}

data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "main" {
  name                      = random_string.main.result
  location                  = azurerm_resource_group.main.location
  resource_group_name       = azurerm_resource_group.main.name
  tenant_id                 = data.azurerm_client_config.current.tenant_id
  sku_name                  = "standard"
  purge_protection_enabled  = false
  enable_rbac_authorization = true
}

resource "azurerm_cdn_frontdoor_profile" "main" {
  name                = random_string.main.result
  resource_group_name = azurerm_resource_group.main.name
  sku_name            = "Standard_AzureFrontDoor"
}

resource "azurerm_eventhub_namespace" "main" {
  name                = random_string.main.result
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "Basic"
}

resource "azurerm_eventhub" "main" {
  name                = "logstream"
  namespace_name      = azurerm_eventhub_namespace.main.name
  resource_group_name = azurerm_resource_group.main.name
  partition_count     = 2
  message_retention   = 1
}

resource "azurerm_eventhub_namespace_authorization_rule" "main" {
  name                = "policy"
  namespace_name      = azurerm_eventhub_namespace.main.name
  resource_group_name = azurerm_resource_group.main.name

  listen = true
  send   = true
  manage = true
}
