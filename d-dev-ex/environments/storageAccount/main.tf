resource "random_string" "main" {
  length  = 4
  special = false
  upper   = false
  lower   = true
  numeric = false
}

locals {
  env_name_cleaned     = replace(lower(var.ade_env_name), "[^a-z]", "")
  storage_account_name = "stc${local.env_name_cleaned}${random_string.main.result}"
}

resource "azurerm_storage_account" "main" {
  name                     = "stc${random_string.main.result}"
  resource_group_name      = var.resource_group_name
  location                 = var.ade_location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}


