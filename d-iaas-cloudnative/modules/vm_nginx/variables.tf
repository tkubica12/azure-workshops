variable "location" {
  description = "The Azure Region in which all resources will be created."
  type        = string
  default     = "swedencentral"
}

variable "resource_group_name" {
  description = "The name of the resource group in which the resources will be created."
  type        = string
}

variable "prefixes" {
  description = "List of prefixes to be used for all resources."
  type        = list(string)
}

variable "image_id" {
  description = <<EOF
The ID of the image to use for the Virtual Machine Scale Set.
If custom image is provider, VMSS will be deployed with it, do not attempt to do pre-installations and turn off automatic guest patching which is not supported.
If not set, modul will deploy plain Ubuntu 22.04 image, automate installation of packages on VM creation time and enable automatic guest patching.
EOF
  type        = string
  default     = null
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

variable "dce_id" {
  description = "The ID of the Data Collection Endpoint to use for monitoring."
  type        = string
}

variable "dcr_id" {
  description = "The ID of the Data Collection Rule to use for monitoring."
  type        = string
}