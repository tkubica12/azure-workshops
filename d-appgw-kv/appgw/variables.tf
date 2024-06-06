variable "resource_group_name" {
  type        = string
  description = "The name of the resource group in which to create the resources"
}

variable "location" {
  type        = string
  description = "The location/region where the resources will be created"
}

variable "subnet_id_kv" {
  type = string
}

variable "subnet_id_appgw" {
  type = string
}

variable "privatedns_id" {
  type = string
}
