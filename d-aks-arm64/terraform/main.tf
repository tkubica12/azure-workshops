// Random string
resource "random_string" "random" {
  length  = 12
  special = false
  upper   = false
  numeric = false
}

// Resource group
resource "azurerm_resource_group" "main" {
  name     = "d-aks-arm64"
  location = "westeurope"
}

// Azure Container Registry
resource "azurerm_container_registry" "main" {
  name                = random_string.random.result
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Basic"
}

// Azure Kubernetes Service
resource "azurerm_kubernetes_cluster" "main" {
  name                = random_string.random.result
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = random_string.random.result
  kubernetes_version  = "1.24"
  node_resource_group = "d-aks-arm64-nodes"

  default_node_pool {
    name       = "amd64"
    node_count = 1
    vm_size    = "Standard_B2ms"
  }

  identity {
    type = "SystemAssigned"
  }
}

// ARM64 node pool
resource "azurerm_kubernetes_cluster_node_pool" "main" {
  name                  = "arm64"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main.id
  vm_size               = "Standard_D2pds_v5"
  node_count            = 1
}

// RBAC for AKS to access ACR
resource "azurerm_role_assignment" "main" {
  scope                = azurerm_container_registry.main.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.main.kubelet_identity[0].object_id
}

output "acr_name" {
  value = azurerm_container_registry.main.name
}

output "aks_name" {
  value = azurerm_kubernetes_cluster.main.name
}

output "rg_name" {
  value = azurerm_resource_group.main.name
}
  
