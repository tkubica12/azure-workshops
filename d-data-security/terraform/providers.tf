terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3"
    }
    azapi = {
      source  = "Azure/azapi"
      version = "~>1"
    }
    random = {
      source  = "hashicorp/random"
      version = "~>3"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~>2"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
    key_vault {
      purge_soft_delete_on_destroy                            = false
      purge_soft_deleted_hardware_security_modules_on_destroy = false
      purge_soft_deleted_certificates_on_destroy              = false
      purge_soft_deleted_keys_on_destroy                      = false
      purge_soft_deleted_secrets_on_destroy                   = false
      recover_soft_deleted_key_vaults                         = true
      recover_soft_deleted_certificates                       = false
      recover_soft_deleted_keys                               = false
      recover_soft_deleted_secrets                            = false
    }
  }
}

provider "azapi" {
}

provider "random" {
}

provider "kubernetes" {
  host                   = azurerm_kubernetes_cluster.main[0].kube_config.0.host
  client_certificate     = base64decode(azurerm_kubernetes_cluster.main[0].kube_config.0.client_certificate)
  client_key             = base64decode(azurerm_kubernetes_cluster.main[0].kube_config.0.client_key)
  cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.main[0].kube_config.0.cluster_ca_certificate)
}