variable "prefix" {
  type        = string
  default     = "apim"
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

variable "REDIRECT_PATH" {
  type        = string
  description = "Redirect path"
  default     = "/auth_response"
}

variable "CUSTOM_API_ENDPOINT" {
  type        = string
  description = "Custom API endpoint"
  default     = "http://localhost:5001"
}

variable "FLASK_SECRET_KEY" {
  type        = string
  description = "Flask secret key"
  default     = "super_secret_key"
}

variable "PAGE_NAME" {
  type        = string
  description = "Page name"
  default     = "Demo"
}

variable "TENANT_ID" {
  type        = string
  description = "Tenant ID"
  default     = "6ce4f237-667f-43f5-aafd-cbef954adf97"
}

variable "byo_app_registrations" {
  type        = bool
  default     = false
  description = "Set to true to bring your own application registrations."
}

variable "app_registrations" {
  type = map(object({
    client_id     = string
    client_secret = string
    uri           = string
  }))
  default = {}
  description = <<EOF
Map of application registrations with client IDs, secrets, and URIs.

Required when 'byo_app_registrations' is true.

Expected keys:
- main
- api
- background
- apim

Each value should be an object with:
- client_id (string)
- client_secret (string)
- Optional: uri (string) - this is for api which exposes APIs

Example:
{
  main = {
    client_id     = "YOUR_MAIN_APP_CLIENT_ID"
    client_secret = "YOUR_MAIN_APP_CLIENT_SECRET"
  },
  api = {
    client_id     = "YOUR_API_APP_CLIENT_ID"
    client_secret = "YOUR_API_APP_CLIENT_SECRET"
    uri           = "api://YOUR_API_APP_URI"
  },
  background = {
    client_id     = "YOUR_BACKGROUND_APP_CLIENT_ID"
    client_secret = "YOUR_BACKGROUND_APP_CLIENT_SECRET"
  },
  apim = {
    client_id     = "YOUR_APIM_APP_CLIENT_ID"
    client_secret = "YOUR_APIM_APP_CLIENT_SECRET"
  }
}
EOF

  validation {
    condition = length(var.app_registrations) == 0 || (
      contains(keys(var.app_registrations), "main") &&
      contains(keys(var.app_registrations), "api") &&
      contains(keys(var.app_registrations), "background") &&
      contains(keys(var.app_registrations), "apim")
    )
    error_message = "When set must include keys 'main', 'api', 'background', and 'apim'."
  }
}