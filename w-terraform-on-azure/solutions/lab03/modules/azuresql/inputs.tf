variable "prefix" {
  type = string
}

variable "location" {
  type = string
}

variable "resourceGroupName" {
  type = string
}

variable "keyVaultId" {
  type = string
}

variable "subnetId" {
  type = string
}

variable "dnsZoneId" {
  type = string
}

variable "readScale" {
  type = bool
  default = false
}

variable "zoneRedundant" {
  type = bool
  default = false
}

variable "skuName" {
  type = string
  default = "S0"
}

variable "dbName" {
  type = string
}

variable "logWorkspaceId" {
  type = string
  default = ""
}

variable "enableAudit" {
  type = bool
  default = false
}