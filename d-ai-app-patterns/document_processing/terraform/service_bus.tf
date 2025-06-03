resource "azurerm_servicebus_namespace" "main" {
  name                = "sb-${local.base_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "Standard"
  local_auth_enabled  = false
}

resource "azurerm_servicebus_queue" "main" {
  name                 = "documents-to-process"
  namespace_id         = azurerm_servicebus_namespace.main.id
  partitioning_enabled = true
}
