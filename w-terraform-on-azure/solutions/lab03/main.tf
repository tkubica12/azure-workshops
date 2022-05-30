// Resource Group
resource "azurerm_resource_group" "demo" {
  name     = "lab03rg"
  location = "westeurope"
}

locals {
  databases = {
    tomdb1 = {
      skuName = "S0"
      dbName = "db1"
    }
    tomdb2 = {
      skuName = "S0"
      dbName = "db2"
    }
    tomdb3 = {
      skuName = "S0"
      dbName = "db3"
    }
  }
}

module "sql" {
  source            = "./modules/azuresql"
  for_each          = yamldecode(file("databases.yaml"))["databases"]
  prefix            = each.key
  resourceGroupName = azurerm_resource_group.demo.name
  location          = azurerm_resource_group.demo.location
  keyVaultId        = azurerm_key_vault.kv.id
  subnetId          = azurerm_subnet.db.id
  dnsZoneId         = azapi_resource.privatednssql.id
  dbName            = each.value["dbName"]
  skuName           = each.value["skuName"]
}
