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

variable "image_id" {
  description = "The ID of the image to use for the Virtual Machine Scale Set."
  type        = string
}

variable "vm_size" {
  description = "The size of the Virtual Machine."
  type        = string
  default     = "Standard_B1s"
}

variable "subnet_id" {
  description = "The ID of the subnet in which the Virtual Machine will be placed."
  type        = string
}