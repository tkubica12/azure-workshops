resource "azurerm_eventhub_namespace" "main" {
  name                = module.main_naming.eventhub_namespace.name_unique
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "Standard"
  capacity            = 1
}

resource "azurerm_eventhub" "main" {
  name                = "sqlaudit"
  namespace_name      = azurerm_eventhub_namespace.main.name
  resource_group_name = azurerm_resource_group.main.name
  partition_count     = 10
  message_retention   = 7
}

resource "azurerm_eventhub_namespace_authorization_rule" "main" {
  name                = "diagnostics"
  namespace_name      = azurerm_eventhub_namespace.main.name
  resource_group_name = azurerm_resource_group.main.name
  listen              = true
  send                = true
  manage              = true
}

resource "azurerm_eventhub_consumer_group" "main" {
  name                = "adx-consumergroup"
  namespace_name      = azurerm_eventhub_namespace.main.name
  eventhub_name       = azurerm_eventhub.main.name
  resource_group_name = azurerm_resource_group.main.name
}


