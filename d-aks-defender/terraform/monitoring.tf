resource "azurerm_log_analytics_workspace" "main" {
  name                = random_string.main.result
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_log_analytics_workspace" "hybrid" {
  name                = "hybrid-${random_string.main.result}"
  location            = azurerm_resource_group.hybrid.location
  resource_group_name = azurerm_resource_group.hybrid.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}