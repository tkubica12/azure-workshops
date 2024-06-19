variable "account_replication_type" {
  type        = string
  description = "The type of replication to use for this storage account. Can be either 'LRS' or 'GRS'."
  default     = "LRS"

  validation {
    condition     = contains(["LRS", "GRS"], var.account_replication_type)
    error_message = "The account_replication_type must be either 'LRS' or 'GRS'."
  }
}


variable "resource_group_name" {
  type        = string
  description = "The name of the resource group in which to create the storage account."
}

variable "ade_env_name" {
  type        = string
}

variable "ade_location" {
  type        = string
}