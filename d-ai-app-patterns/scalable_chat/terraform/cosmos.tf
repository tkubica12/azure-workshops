resource "azurerm_cosmosdb_account" "main" {
  name                          = "cosmos-${local.base_name}"
  location                      = azurerm_resource_group.main.location
  resource_group_name           = azurerm_resource_group.main.name
  kind                          = "GlobalDocumentDB"
  offer_type                    = "Standard"
  local_authentication_disabled = true
  public_network_access_enabled = true

  capabilities {
    name = "EnableServerless"
  }

  capabilities {
    name = "EnableNoSQLVectorSearch"
  }

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = azurerm_resource_group.main.location
    failover_priority = 0
  }
}
