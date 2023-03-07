// Shared disk
resource "azurerm_managed_disk" "main" {
  name                 = "shared-disk"
  location             = azurerm_resource_group.main.location
  resource_group_name  = azurerm_resource_group.main.name
  storage_account_type = "Premium_LRS"
  create_option        = "Empty"
  disk_size_gb         = 16
  max_shares           = 2
}

// Attach disk to vm1
