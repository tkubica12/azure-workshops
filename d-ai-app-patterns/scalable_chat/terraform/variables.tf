variable "llm_location" {
  type        = string
  default     = "swedencentral"
  description = "Azure region for LLM-related resources."
}
variable "prefix" {
  type        = string
  default     = "chat"
  description = <<EOF
Prefix for resources.
Preferably 2-4 characters long without special characters, lowercase.
EOF
}

variable "location" {
  type        = string
  default     = "germanywestcentral"
  description = <<EOF
Azure region for resources.

Examples: swedencentral, westeurope, northeurope, germanywestcentral.
EOF
}

variable "service_bus_sku" {
  type        = string
  default     = "Premium"
  description = "Service Bus SKU: Standard or Premium"
  validation {
    condition     = contains(["Standard", "Premium"], var.service_bus_sku)
    error_message = "SKU must be either 'Standard' or 'Premium'."
  }
}