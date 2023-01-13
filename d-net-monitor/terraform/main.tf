resource "azurerm_resource_group" "main" {
  name     = "d-net-monitor"
  location = var.location1
}

resource "random_string" "main" {
  length  = 12
  special = false
  upper   = false
  lower   = true
  numeric = false
}
