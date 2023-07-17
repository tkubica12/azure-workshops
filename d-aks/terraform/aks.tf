resource "azurerm_kubernetes_cluster" "aks1" {
  name                 = "d-aks"
  location             = azurerm_resource_group.main.location
  resource_group_name  = azurerm_resource_group.main.name
  dns_prefix           = "d-aks"
  azure_policy_enabled = true
  
  azure_active_directory_role_based_access_control {
    managed            = true
    azure_rbac_enabled = true
  }

  default_node_pool {
    name                        = "default"
    node_count                  = 2
    enable_auto_scaling         = true
    min_count                   = 2
    max_count                   = 5
    vm_size                     = "Standard_B4ms"
    temporary_name_for_rotation = "defaulttemp"
  }

  identity {
    type = "SystemAssigned"
  }

  workload_autoscaler_profile {
    keda_enabled                    = true
    vertical_pod_autoscaler_enabled = true
  }

  monitor_metrics {}

  oms_agent {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
  }

  # service_mesh_profile {
  #   mode                             = "Istio"
  #   internal_ingress_gateway_enabled = false
  #   external_ingress_gateway_enabled = false
  # }

  lifecycle {
    ignore_changes = [
      azure_policy_enabled,
      microsoft_defender
    ]
  }
}

resource "azurerm_role_assignment" "aks1" {
  scope                = azurerm_kubernetes_cluster.aks1.id
  role_definition_name = "Azure Kubernetes Service RBAC Cluster Admin"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_kubernetes_cluster_extension" "aks1" {
  name           = "flux"
  cluster_id     = azurerm_kubernetes_cluster.aks1.id
  extension_type = "microsoft.flux"
}

resource "azurerm_kubernetes_flux_configuration" "aks1" {
  name       = "my-flux-config"
  cluster_id = azurerm_kubernetes_cluster.aks1.id
  namespace  = "flux-system"
  scope      = "cluster"

  git_repository {
    url                      = "https://github.com/tkubica12/azure-workshops"
    reference_type           = "branch"
    reference_value          = "main"
    sync_interval_in_seconds = 120
    timeout_in_seconds       = 120
  }

  kustomizations {
    name                       = "my-kustomization1"
    path                       = "d-aks/kubernetes/clusters/d-aks"
    sync_interval_in_seconds   = 120
    retry_interval_in_seconds  = 120
    timeout_in_seconds         = 300
    recreating_enabled         = true
    garbage_collection_enabled = true
  }

  depends_on = [
    azurerm_kubernetes_cluster_extension.aks1
  ]
}

resource "azurerm_kubernetes_cluster" "aks2" {
  name                = "d-aks-us"
  location            = "westus"
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "d-aks-us"

  default_node_pool {
    name                        = "default"
    node_count                  = 1
    vm_size                     = "Standard_B4ms"
    temporary_name_for_rotation = "defaulttemp"
  }

  identity {
    type = "SystemAssigned"
  }

  lifecycle {
    ignore_changes = [
      azure_policy_enabled,
      microsoft_defender
    ]
  }
}

resource "azurerm_role_assignment" "aks2" {
  scope                = azurerm_kubernetes_cluster.aks2.id
  role_definition_name = "Azure Kubernetes Service RBAC Cluster Admin"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_kubernetes_cluster_extension" "aks2" {
  name           = "flux"
  cluster_id     = azurerm_kubernetes_cluster.aks2.id
  extension_type = "microsoft.flux"
}
