resource "azurerm_resource_group" "workshop" {
  name     = "shared-workshop-resources"
  location = "West Europe"
}

# resource "azurerm_management_lock" "workshop" {
#   name       = "do-not-delete"
#   scope      = azurerm_resource_group.workshop.id
#   lock_level = "CanNotDelete"
#   notes      = "Shared resources for workshop"
# }