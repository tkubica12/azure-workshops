variable "prefix" {
  type        = string
  default     = "aiasync"
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

variable "azure_openai_api_key" {
  type        = string
  description = "API key for Azure OpenAI"
  sensitive   = true
}

variable "azure_openai_endpoint" {
  type        = string
  description = "Endpoint for Azure OpenAI"
}
