
# Create Azure Cosmos DB account
resource "azurerm_cosmosdb_account" "main" {
  name                          = "${local.base_name}-cosmosdb"
  location                      = azurerm_resource_group.main.location
  resource_group_name           = azurerm_resource_group.main.name
  offer_type                    = "Standard"
  kind                          = "GlobalDocumentDB"
  local_authentication_disabled = true

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = azurerm_resource_group.main.location
    failover_priority = 0
  }
}

# # Grant managed identity access to CosmosDB
# resource "azurerm_role_assignment" "cosmosdb_access" {
#   principal_id         = azurerm_user_assigned_identity.main.principal_id
#   role_definition_name = "Cosmos DB Account Reader Role"
#   scope                = azurerm_cosmosdb_account.main.id
# }

