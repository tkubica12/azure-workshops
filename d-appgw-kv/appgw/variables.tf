variable "resource_group_name" {
  type        = string
  description = "The name of the resource group in which to create the resources"
}

variable "location" {
  type        = string
  description = "The location/region where the resources will be created"
}

variable "keyvault_id" {
  type        = string
  description = "The ID of the Key Vault to which the App Gateway will be granted access"
}