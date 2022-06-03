resource "random_string" "logs" {
  length  = 16
  special = false
  upper   = false
  lower   = true
  number  = false
}

resource "azurerm_log_analytics_workspace" "logs" {
  name                = random_string.logs.result
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}
