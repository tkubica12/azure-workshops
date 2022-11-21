terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3"
    }
    random = {
      source  = "hashicorp/random"
      version = "~>3"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~>2"
    }
    azapi = {
      source  = "azure/azapi"
      version = "~>1"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
    log_analytics_workspace {
      permanently_delete_on_destroy = true
    }
    virtual_machine {
      skip_shutdown_and_force_delete = true
    }
  }
}
