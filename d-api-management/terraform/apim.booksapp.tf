resource "azurerm_api_management_api" "booksapp" {
  name                  = "BooksApp"
  resource_group_name   = azurerm_resource_group.main.name
  api_management_name   = azurerm_api_management.main.name
  revision              = "1"
  display_name          = "BooksApp"
  path                  = "api"
  protocols             = ["https"]
  subscription_required = false
}
