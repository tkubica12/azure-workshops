resource "azurerm_cosmosdb_sql_database" "memory" {
  name                = "memory"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}

resource "azapi_resource" "memory_conversations" {
  type      = "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2025-05-01-preview"
  name      = "conversations"
  parent_id = azurerm_cosmosdb_sql_database.memory.id

  body = {
    properties = {
      resource = {
        id = "conversations"
        partitionKey = {
          paths = ["/userId"]
          kind  = "Hash"
        }
        vectorEmbeddingPolicy = {
          vectorEmbeddings = [
            {
              dataType = "float32"
              dimensions = 3072
              distanceFunction = "cosine"
              path = "/vector_embedding"
            }
          ]
        }
        indexingPolicy = {
          indexingMode = "consistent"
          automatic = true
          includedPaths = [
            {
              path = "/*"
            }
          ]
          excludedPaths = [
            {
              path = "/vector_embedding/*"
            }
          ]
          vectorIndexes = [
            {
              path = "/vector_embedding"
              type = "diskANN"
            }
          ]
        }
      }
    }
  }
}

resource "azapi_resource" "memory_user_memories" {
  type      = "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2025-05-01-preview"
  name      = "user-memories"
  parent_id = azurerm_cosmosdb_sql_database.memory.id

  body = {
    properties = {
      resource = {
        id = "user-memories"
        partitionKey = {
          paths = ["/userId"]
          kind  = "Hash"
        }
      }
    }
  }
}
