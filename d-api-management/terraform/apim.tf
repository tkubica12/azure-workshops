resource "azurerm_api_management" "main" {
  name                = "apim-${local.base_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  publisher_name      = "My Company"
  publisher_email     = "company@company.local"

  sku_name = "Developer_1"
}
