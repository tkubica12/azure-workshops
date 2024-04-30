variable "location" {
  description = "The Azure Region in which all resources will be created."
  type        = string
  default     = "swedencentral"
}

variable "resource_group_name" {
  description = "The name of the resource group in which the resources will be created."
  type        = string
}

variable "prefix" {
  description = "The prefix to be used for all resources."
  type        = string
}
