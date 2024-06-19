resource "random_string" "main" {
  length  = 6
  special = false
  upper   = false
  lower   = true
  numeric = false
}

resource "azurerm_resource_group" "main" {
  name     = "rg-${random_string.main.result}"
  location = "swedencentral"
}

resource "azurerm_storage_account" "main" {
  name                     = "stc${random_string.main.result}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}


