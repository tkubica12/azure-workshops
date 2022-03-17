resource "azurerm_log_analytics_workspace" "workshop" {
  name                = "workshop-sdkjngfel4574346"
  location            = azurerm_resource_group.workshop.location
  resource_group_name = azurerm_resource_group.workshop.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_automation_account" "workshop" {
  name                = "automation"
  location            = azurerm_resource_group.workshop.location
  resource_group_name = azurerm_resource_group.workshop.name

  sku_name = "Basic"
}

resource "azurerm_log_analytics_linked_service" "workshop" {
  resource_group_name = azurerm_resource_group.workshop.name
  workspace_id        = azurerm_log_analytics_workspace.workshop.id
  read_access_id      = azurerm_automation_account.workshop.id
}

resource "azurerm_log_analytics_solution" "containers" {
  solution_name         = "VMInsights"
  location              = azurerm_resource_group.workshop.location
  resource_group_name   = azurerm_resource_group.workshop.name
  workspace_resource_id = azurerm_log_analytics_workspace.workshop.id
  workspace_name        = azurerm_log_analytics_workspace.workshop.name

  plan {
    publisher = "Microsoft"
    product   = "OMSGallery/VMInsights"
  }
}

resource "azurerm_log_analytics_solution" "SecurityInsights" {
  solution_name         = "SecurityInsights"
  location              = azurerm_resource_group.workshop.location
  resource_group_name   = azurerm_resource_group.workshop.name
  workspace_resource_id = azurerm_log_analytics_workspace.workshop.id
  workspace_name        = azurerm_log_analytics_workspace.workshop.name

  plan {
    publisher = "Microsoft"
    product   = "OMSGallery/SecurityInsights"
  }
}

resource "azurerm_recovery_services_vault" "workshop" {
  name                = "backup-vault"
  location            = azurerm_resource_group.workshop.location
  resource_group_name = azurerm_resource_group.workshop.name
  sku                 = "Standard"
  soft_delete_enabled = false
}


# data "azurerm_subscription" "current" {
# }

# resource "azurerm_security_center_workspace" "workshop" {
#   scope        = data.azurerm_subscription.current.id
#   workspace_id = azurerm_log_analytics_workspace.workshop.id
# }

# resource "azurerm_security_center_auto_provisioning" "workshop" {
#   auto_provision = "On"
# }
