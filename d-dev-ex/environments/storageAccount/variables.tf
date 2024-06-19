variable "account_replication_type" {
  type        = string
  description = "The type of replication to use for this storage account. Can be either 'LRS' or 'GRS'."
  default     = "LRS"

  validation {
    condition     = contains(["LRS", "GRS"], var.account_replication_type)
    error_message = "The account_replication_type must be either 'LRS' or 'GRS'."
  }
}
