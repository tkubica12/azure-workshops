variable "prefix" {
  type        = string
  default     = "apim-genai"
  description = <<EOF
Prefix for resources.
Preferably 2-4 characters long without special characters, lowercase.
EOF
}

variable "location" {
  type        = string
  default     = "swedencentral"
  description = <<EOF
Azure region for resources.

Examples: swedencentral, westeurope, northeurope, germanywestcentral.
EOF
}

variable "apim_sku" {
  type        = string
  default     = "Premium_1"
  description = <<EOF
Azure API Management SKU.

Examples: Developer_1, Standard_1, Premium_1.
EOF
}
