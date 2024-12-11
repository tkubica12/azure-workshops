variable "app_registrations" {
  type = bool
  description = "Condition for app registrations"
  default = false
  condition = var.app_registrations
}