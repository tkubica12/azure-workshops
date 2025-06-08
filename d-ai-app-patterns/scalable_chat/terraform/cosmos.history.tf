resource "azurerm_cosmosdb_sql_database" "history" {
  name                = "history"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}

resource "azapi_resource" "history_conversations" {
  type      = "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2025-05-01-preview"
  name      = "conversations"
  parent_id = azurerm_cosmosdb_sql_database.history.id

  body = {
    properties = {
      resource = {
        id = "conversations"
        partitionKey = {
          paths = ["/sessionId"]
          kind  = "Hash"
        }
      }
    }
  }
}
