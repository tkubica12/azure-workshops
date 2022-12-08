resource "azurerm_kubernetes_cluster" "aks1" {
  name                = "d-kubecost"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "d-kubecost"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_B2ms"

    node_labels = {
      L1 = "A"
    }
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    L1 = "A"
  }
}

resource "azurerm_kubernetes_cluster_node_pool" "aks1_pool1" {
  name                  = "pool1"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks1.id
  vm_size               = "Standard_B2ms"
  node_count            = 2

  tags = {
    L1 = "A"
    L2 = "A"
  }

  node_labels = {
    L1 = "A"
    L2 = "A"
  }
}

resource "azurerm_kubernetes_cluster_node_pool" "aks1_pool2" {
  name                  = "pool2"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks1.id
  vm_size               = "Standard_B2ms"
  node_count            = 1

  tags = {
    L1 = "A"
    L2 = "B"
  }

  node_labels = {
    L1 = "A"
    L2 = "B"
  }
}
