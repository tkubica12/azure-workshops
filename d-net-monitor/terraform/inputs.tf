variable "location1" {
  type    = string
  default = "westeurope"
}

variable "location2" {
  type    = string
  default = "northeurope"
}

variable "admin_password" {
  type      = string
  sensitive = true
  default   = "Azure12345678"
}

variable "existing_watcher_name_location1" {
  type = string
  default = ""
  description = "There can be just watcher per region. Leave blank if you want to create a new one, specify id if you have one already"
}

variable "existing_watcher_rg_location1" {
  type = string
  default = ""
  description = "There can be just watcher per region. Leave blank if you want to create a new one, specify id if you have one already"
}

variable "existing_watcher_name_location2" {
  type = string
  default = ""
  description = "There can be just watcher per region. Leave blank if you want to create a new one, specify id if you have one already"
}

variable "existing_watcher_rg_location2" {
  type = string
  default = ""
  description = "There can be just watcher per region. Leave blank if you want to create a new one, specify id if you have one already"
}