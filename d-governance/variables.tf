variable "subscription_id" {
  type        = string
  description = "The subscription ID where the policies and RBAC will be applied"
  default     = "d3b7888f-c26e-4961-a976-ff9d5b31dfd3"
}

variable "location" {
  type        = string
  description = "The location where the policies and RBAC will be applied"
  default     = "swedencentral"
}

variable "hub_subscription_id" {
  type        = string
  description = "The subscription ID of the hub subscription"
  default     = "7bead9cf-e290-4c50-8651-fcc22c9c70a5"
}

variable "root_mg_id" {
  type        = string
  description = "The management group ID of the root management group"
  default     = "d6af5f85-2a50-4370-b4b5-9b9a55bcb0dc"
}

variable "user_object_id" {
  type        = string
  description = "The object ID of the user for testing"
  default     = "d140ebb6-f211-4d8d-ac70-c4eedb84b013"
}

