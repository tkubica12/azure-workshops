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

