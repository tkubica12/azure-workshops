resource "azurerm_cognitive_account" "custom_vision" {
  name                = "custom-vision-${random_string.random.result}"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  kind                = "CustomVision.Training"
  sku_name            = "S0"
}

resource "azurerm_cognitive_account" "custom_vision_pred" {
  name                = "custom-vision-pred-${random_string.random.result}"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  kind                = "CustomVision.Prediction"
  sku_name            = "S0"
}
