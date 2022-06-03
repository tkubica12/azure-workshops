// Resource Group
resource "azurerm_resource_group" "demo" {
  name     = var.resoucreGroupName
  location = "westeurope"
}

module "sql" {
  source            = "../../modules/azuresql"
  for_each          = var.databases
  prefix            = each.key
  resourceGroupName = azurerm_resource_group.demo.name
  location          = azurerm_resource_group.demo.location
  keyVaultId        = azurerm_key_vault.kv.id
  subnetId          = azurerm_subnet.db.id
  dnsZoneId         = azapi_resource.privatednssql.id
  dbName            = each.value["dbName"]
  skuName           = each.value["skuName"]
}
