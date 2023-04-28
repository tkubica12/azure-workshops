// AKS with default node
resource "azurerm_kubernetes_cluster" "main" {
  count               = var.enable_aks ? 1 : 0
  name                = "aks-confidential"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  dns_prefix          = "aks-confidential"

  identity {
    type = "SystemAssigned"
  }

  confidential_computing {
    sgx_quote_helper_enabled = true
  }

  linux_profile {
    admin_username = "tomas"
    ssh_key {
      key_data = file("~/.ssh/id_rsa.pub")
    }
  }

  default_node_pool {
    name           = "default"
    node_count     = 1
    vm_size        = "Standard_B2ms"
    type           = "VirtualMachineScaleSets"
    vnet_subnet_id = azurerm_subnet.main.id
  }

  network_profile {
    network_plugin      = "azure"
    load_balancer_sku   = "standard"
    network_plugin_mode = "Overlay"
    service_cidr        = "192.168.0.0/16"
    dns_service_ip      = "192.168.10.10"
  }
}

// Confidential nodepool
resource "azurerm_kubernetes_cluster_node_pool" "confidential_node" {
  count                 = var.enable_aks ? 1 : 0
  name                  = "sevsnp"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main[0].id
  vm_size               = "Standard_DC2as_v5"
  node_count            = 1
  zones                 = ["2"]
  vnet_subnet_id        = azurerm_subnet.main.id

  node_labels = {
    securetype = "sevsnp"
  }
}

// Nodepool supporting SXG confidential containers
resource "azurerm_kubernetes_cluster_node_pool" "confidential_sxg_containers" {
  count                 = var.enable_aks ? 1 : 0
  name                  = "sgx"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main[0].id
  vm_size               = "Standard_DC2s_v3"
  node_count            = 1
  zones                 = ["1"]
  vnet_subnet_id        = azurerm_subnet.main.id

  node_labels = {
    securetype = "sgx"
  }
}

// Nodepool supporting nested virtualization kata containers
resource "azurerm_kubernetes_cluster_node_pool" "kata" {
  count                 = var.enable_aks ? 1 : 0
  name                  = "kata"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main[0].id
  vm_size               = "Standard_E2s_v3"
  node_count            = 1
  zones                 = ["1"]
  vnet_subnet_id        = azurerm_subnet.main.id
  workload_runtime      = "KataMshvVmIsolation"
  os_sku                = "Mariner"

  node_labels = {
    securetype = "kata"
  }
}

// Nodepool supporting nested virtualization confidential containers

// Pods
resource "kubernetes_pod_v1" "standard_on_sgx" {
  metadata {
    name      = "standard-on-sgx"
    namespace = "default"
  }

  spec {
    container {
      image = "ghcr.io/tkubica12/secure:standard"
      name  = "demo"
    }

    affinity {
      node_affinity {
        required_during_scheduling_ignored_during_execution {
          node_selector_term {
            match_expressions {
              key      = "securetype"
              operator = "In"
              values   = ["sgx"]
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_pod_v1" "standard_on_kata" {
  metadata {
    name      = "standard-on-kata"
    namespace = "default"
  }

  spec {
    runtime_class_name = "kata-mshv-vm-isolation"

    container {
      image = "ghcr.io/tkubica12/secure:standard"
      name  = "demo"
    }

    affinity {
      node_affinity {
        required_during_scheduling_ignored_during_execution {
          node_selector_term {
            match_expressions {
              key      = "securetype"
              operator = "In"
              values   = ["kata"]
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_pod_v1" "standard_on_sevsnp" {
  metadata {
    name      = "standard-on-sevsnp"
    namespace = "default"
  }

  spec {
    container {
      image = "ghcr.io/tkubica12/secure:standard"
      name  = "demo"
    }

    affinity {
      node_affinity {
        required_during_scheduling_ignored_during_execution {
          node_selector_term {
            match_expressions {
              key      = "securetype"
              operator = "In"
              values   = ["sevsnp"]
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_pod_v1" "sgx" {
  metadata {
    name      = "sgx"
    namespace = "default"
  }

  spec {
    container {
      image = "ghcr.io/tkubica12/secure:sgx"
      name  = "demo"

      resources {
        limits = {
          "kubernetes.azure.com/sgx_epc_mem_in_MiB" = 10
        }
        requests = {
          "kubernetes.azure.com/sgx_epc_mem_in_MiB" = 10
        }
      }
    }

    affinity {
      node_affinity {
        required_during_scheduling_ignored_during_execution {
          node_selector_term {
            match_expressions {
              key      = "securetype"
              operator = "In"
              values   = ["sgx"]
            }
          }
        }
      }
    }
  }
}
