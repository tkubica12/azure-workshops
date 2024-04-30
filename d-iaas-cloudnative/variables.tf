variable "location" {
  description = "The Azure Region in which all resources will be created."
  type        = string
  default     = "swedencentral"
}

variable "main_prefix" {
  description = "value to be used as prefix for all resources"
  type        = string
  default     = "demo"
}
