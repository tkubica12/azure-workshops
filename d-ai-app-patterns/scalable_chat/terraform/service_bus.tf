resource "azurerm_servicebus_namespace" "main" {
  name                = "sb-${local.base_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "Standard"
  local_auth_enabled  = false
}

resource "azurerm_servicebus_topic" "user_messages" {
  name                 = "user-messages"
  namespace_id         = azurerm_servicebus_namespace.main.id
  partitioning_enabled = true
}

resource "azurerm_servicebus_topic" "token_streams" {
  name                 = "token-streams"
  namespace_id         = azurerm_servicebus_namespace.main.id
  partitioning_enabled = true
}

resource "azurerm_servicebus_subscription" "front_service" {
  name               = "front-service"
  topic_id           = azurerm_servicebus_topic.token_streams.id
  max_delivery_count = 10
  requires_session   = true
}

resource "azurerm_servicebus_subscription" "worker_service" {
  name               = "worker-service"
  topic_id           = azurerm_servicebus_topic.user_messages.id
  max_delivery_count = 10
  requires_session   = false
}
