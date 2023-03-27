// Resource Group
resource "azurerm_resource_group" "main" {
  name     = "d-storage-files"
  location = var.location
}

resource "azurerm_role_assignment" "fadmin_contributor" {
  scope                = azurerm_resource_group.main.id
  role_definition_name = "Contributor"
  principal_id         = azuread_user.admin.object_id
}

// Random suffix
resource "random_string" "storage" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

// Get current account data
data "azurerm_client_config" "current" {}