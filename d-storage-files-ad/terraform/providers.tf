terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3"
    }
    # azapi = {
    #   source  = "azure/azapi"
    #   version = "~>1"
    # }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~>2"
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
    virtual_machine {
      skip_shutdown_and_force_delete = true
    }
    log_analytics_workspace {
      permanently_delete_on_destroy = true
    }
  }
}
