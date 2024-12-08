variable "location" {
  description = "Location of all resources"
  type        = string
  default     = "swedencentral"
}

variable "secondary_location" {
  description = "Secondary location for geo cluster"
  type        = string
  default     = "germanywestcentral"
}

variable "prefix" {
  description = "Prefix for all resources"
  type        = string
  default     = "redis"
}
