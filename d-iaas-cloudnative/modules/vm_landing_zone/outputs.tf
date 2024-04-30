output "subnet_id" {
  value = azurerm_subnet.main.id
}

output "dce_id" {
  value = azurerm_monitor_data_collection_endpoint.main.id
}

output "dcr_id" {
  value = azurerm_monitor_data_collection_rule.main.id
}