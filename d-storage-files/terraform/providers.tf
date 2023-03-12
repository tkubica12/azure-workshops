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
  }
}
