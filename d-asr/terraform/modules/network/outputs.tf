output "spoke1_id" {
  value = azurerm_virtual_network.spoke1.id
}

output "spoke1_subnet1_id" {
  value = azurerm_subnet.spoke1_vm.id
}