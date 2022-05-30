// Resource Group
resource "azurerm_resource_group" "demo" {
  name     = "lab03rg"
  location = "westeurope"
}

module "sql" {
  source            = "./modules/azuresql"
  prefix            = "tomas"
  resourceGroupName = azurerm_resource_group.demo.name
  location          = azurerm_resource_group.demo.location
  keyVaultId        = azurerm_key_vault.kv.id
  subnetId          = azurerm_subnet.db.id
  dnsZoneId         = azapi_resource.privatednssql.id
  dbName            = "testdb"
  enableAudit       = true
  logWorkspaceId    = azurerm_log_analytics_workspace.logs.id
}