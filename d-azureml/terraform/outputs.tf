output "azureml_workspace_name" {
  value = azurerm_machine_learning_workspace.demo.name
}

output "resource_group_name" {
  value = azurerm_resource_group.demo.name
}

output "acr_name" {
  value = azurerm_container_registry.demo.name
}

  