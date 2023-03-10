variable "location" {
  type    = string
  default = "westeurope"
}

variable "password" {
  type      = string
  default   = "Azure12345678"
  sensitive = true
}
