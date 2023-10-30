terraform {
  required_providers {
    # azurerm = {
    #   source  = "hashicorp/azurerm"
    #   version = "~>3"
    # }
    azapi = {
      source  = "azure/azapi"
      version = "~>1"
    }
    random = {
      source  = "hashicorp/random"
      version = "~>3"
    }
  }
}