variable "main_region" {
  description = "The main region where the resources will be created"
  type        = string
  default     = "germanywestcentral"
}

variable "target_region" {
  description = "The target fully capable region where applications will be recovered in case of a disaster"
  type        = string
  default     = "swedencentral"
}

variable "storage_region" {
  description = "Intermediate region that is paired to main region, but not fully capable to host applications in case of a disaster"
  type        = string
  default     = "germanynorth"
}

variable "directreplication_scenario" {
  description = "Enable direct replication scenarios - main to target replication"
  type        = bool
  default     = true
}

variable "indirectreplication_scenario" {
  description = "Enable indirect replication scenarios - main to storage in pair region replication and then to target region"
  type        = bool
  default     = true
}

variable "sql_scenario" {
  description = "Enable SQL scenario"
  type        = bool
  default     = true
}

variable "storage_scenario" {
  description = "Enable SQL scenario"
  type        = bool
  default     = true
}

variable "psql_scenario" {
  description = "Enable PostgreSQL scenario"
  type        = bool
  default     = true
}

variable "vm_scenario" {
  description = "Enable Azure VM scenario"
  type        = bool
  default     = true
}
