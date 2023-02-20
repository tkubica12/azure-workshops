# resource "azurerm_eventhub_cluster" "dedicated" {
#   name                = "${random_string.main.result}-dedicated"
#   resource_group_name = azurerm_resource_group.main.name
#   location            = azurerm_resource_group.main.location
#   sku_name            = "Dedicated_1"
# }

# resource "azurerm_eventhub_namespace" "standard" {
#   name                     = "${random_string.main.result}-standard"
#   location                 = azurerm_resource_group.main.location
#   resource_group_name      = azurerm_resource_group.main.name
#   sku                      = "Standard"
#   auto_inflate_enabled     = true
#   maximum_throughput_units = 20
#   capacity                 = 2
# }

# resource "azurerm_eventhub_namespace" "premium" {
#   name                = "${random_string.main.result}-premium"
#   location            = azurerm_resource_group.main.location
#   resource_group_name = azurerm_resource_group.main.name
#   sku                 = "Premium"
#   zone_redundant      = true
# }
