
# Create Azure Cosmos DB account
resource "azurerm_cosmosdb_account" "main" {
  name                          = "${local.base_name}-cosmosdb"
  location                      = azurerm_resource_group.main.location
  resource_group_name           = azurerm_resource_group.main.name
  offer_type                    = "Standard"
  kind                          = "GlobalDocumentDB"
  local_authentication_disabled = true

  capabilities {
    name = "EnableServerless"
  }

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = azurerm_resource_group.main.location
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_sql_database" "booksapp" {
  name                = "BooksApp"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}

resource "azurerm_cosmosdb_sql_container" "books" {
  name                  = "Books"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  database_name         = azurerm_cosmosdb_sql_database.booksapp.name
  partition_key_paths   = ["/id"]
  partition_key_version = 2
}

resource "azurerm_cosmosdb_sql_container" "lists" {
  name                  = "Lists"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  database_name         = azurerm_cosmosdb_sql_database.booksapp.name
  partition_key_paths   = ["/id"]
  partition_key_version = 2
}

resource "azurerm_cosmosdb_sql_container" "reviews" {
  name                  = "Reviews"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  database_name         = azurerm_cosmosdb_sql_database.booksapp.name
  partition_key_paths   = ["/id"]
  partition_key_version = 2
}