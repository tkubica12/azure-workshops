resource "azurerm_kubernetes_cluster" "main" {
  name                 = "d-aks-defender"
  location             = azurerm_resource_group.main.location
  resource_group_name  = azurerm_resource_group.main.name
  dns_prefix           = "d-aks-defender"
  azure_policy_enabled = true

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_B2ms"
  }

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.main.id
    ]
  }

  kubelet_identity {
    user_assigned_identity_id = azurerm_user_assigned_identity.main.id
    client_id                 = azurerm_user_assigned_identity.main.client_id
    object_id                 = azurerm_user_assigned_identity.main.principal_id
  }

  microsoft_defender {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
  }
}

resource "azurerm_user_assigned_identity" "main" {
  name                = "identity"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_role_assignment" "identityoperator" {
  scope                = azurerm_user_assigned_identity.main.id
  role_definition_name = "Managed Identity Operator"
  principal_id         = azurerm_user_assigned_identity.main.principal_id
}