terraform {
  backend "local" {}
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3"
    }
    random = {
      source  = "hashicorp/random"
      version = "~>3"
    }
  }
}

provider "azurerm" {
  use_oidc = true
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}
