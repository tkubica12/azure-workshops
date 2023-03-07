// Resource Group
resource "azurerm_resource_group" "main" {
  name     = "d-storage-disk-shared"
  location = var.location
}