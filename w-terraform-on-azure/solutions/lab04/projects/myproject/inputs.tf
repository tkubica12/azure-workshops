# Database map
/*
databases:
  tomdb1:
    skuName: S0
    dbName: db1
  tomdb2:
    skuName: S0
    dbName: db2
  tomdb3:
    skuName: S0
    dbName: db3
*/

variable "databases" {
  type = map(map(string))
}

# Resource group name
variable "resoucreGroupName" {
  type = string
}