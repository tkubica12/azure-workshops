// Shared disk
resource "azurerm_managed_disk" "main" {
  name                 = "shared-disk"
  location             = azurerm_resource_group.main.location
  resource_group_name  = azurerm_resource_group.main.name
  storage_account_type = "Premium_ZRS"
  create_option        = "Empty"
  disk_size_gb         = 16
  max_shares           = 2
}

// Attach disk to vm1
resource "azurerm_virtual_machine_data_disk_attachment" "vm1" {
  managed_disk_id    = azurerm_managed_disk.main.id
  virtual_machine_id = azurerm_linux_virtual_machine.vm1.id
  lun                = "0"
  caching            = "None"
}

// Attach disk to vm2
resource "azurerm_virtual_machine_data_disk_attachment" "vm2" {
  managed_disk_id    = azurerm_managed_disk.main.id
  virtual_machine_id = azurerm_linux_virtual_machine.vm2.id
  lun                = "0"
  caching            = "None"

  depends_on = [
    azurerm_virtual_machine_data_disk_attachment.vm1
  ]
}