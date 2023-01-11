output "azureml_workspace_name" {
  value = azurerm_machine_learning_workspace.demo.name
}

output "resource_group_name" {
  value = azurerm_resource_group.demo.name
}

output "acr_name" {
  value = azurerm_container_registry.demo.name
}

output "aksid" {
  value = var.deploy_aks ? azurerm_kubernetes_cluster.demo[0].id : ""
}

output "amlidentity" {
  value = azurerm_user_assigned_identity.aml.id
}

output "custom_vision_name" {
  value = azurerm_cognitive_account.custom_vision.name
}

  
