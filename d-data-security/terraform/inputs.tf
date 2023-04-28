variable "current_user_name" {
  type        = string
  description = "The name of the current user"
  default     = "admin@tkubica.biz"
}
  
variable "enable_ade" {
  type = bool
}
  
variable "enable_sse" {
  type = bool
}
  
variable "enable_sql" {
  type = bool
}
  
variable "enable_ledger" {
  type = bool
}
  
variable "enable_storage" {
  type = bool
}
  
variable "enable_confidential_vm" {
  type = bool
}
  
variable "enable_bastion" {
  type = bool
}
  
variable "enable_aks" {
  type = bool
}