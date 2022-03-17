resource "azurerm_resource_group" "demo" {
  name     = "${var.prefix}-automation"
  location = "westeurope"
}
