resource "random_string" "random" {
  length  = 12
  special = false
  upper   = false
}

resource "azurerm_servicebus_namespace" "demo" {
  name                = "sb${random_string.random.result}"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  sku                 = "Basic"
}

resource "azurerm_servicebus_queue" "orders" {
  name         = "orders"
  namespace_id = azurerm_servicebus_namespace.demo.id
}

resource "azurerm_servicebus_queue_authorization_rule" "demo" {
  name     = "demo"
  queue_id = azurerm_servicebus_queue.orders.id

  listen = true
  send   = true
  manage = false
}