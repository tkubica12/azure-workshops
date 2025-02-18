terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>4"
    }
    random = {
      source  = "hashicorp/random"
      version = "~>3"
    }
    azapi = {
      source  = "Azure/azapi"
      version = "~>2"
    }
  }
}

provider "azurerm" {
  subscription_id     = "673af34d-6b28-41dc-bc7b-f507418045e6"
  storage_use_azuread = true

  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }

    key_vault {
      purge_soft_delete_on_destroy               = true
      purge_soft_deleted_secrets_on_destroy      = true
      purge_soft_deleted_certificates_on_destroy = true
      recover_soft_deleted_secrets               = true
      recover_soft_deleted_certificates          = true
      recover_soft_deleted_key_vaults            = true
    }

    api_management {
      purge_soft_delete_on_destroy = true
      recover_soft_deleted         = true
    }

    cognitive_account {
      purge_soft_delete_on_destroy = true
    }

    # storage {
    #   data_plane_available = false
    # }
  }
}

provider "random" {
  # Configuration options
}

