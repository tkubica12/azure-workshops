resource "random_uuid" "cosmosdb_role_assignment_guid_self" {}
resource "random_uuid" "cosmosdb_role_assignment_guid_app" {}
resource "random_uuid" "cosmosdb_role_assignment_guid_history_worker" {}
resource "random_uuid" "cosmosdb_role_assignment_guid_memory_api" {}
resource "random_uuid" "cosmosdb_role_assignment_guid_memory_worker" {}
resource "random_uuid" "cosmosdb_role_assignment_guid_history_api" {}

resource "azurerm_cosmosdb_sql_role_definition" "main" {
  name                = "mywriter"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  type                = "CustomRole"
  assignable_scopes   = [azurerm_cosmosdb_account.main.id]

  permissions {
    data_actions = [
      "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*",
      "Microsoft.DocumentDB/databaseAccounts/readMetadata"
    ]
  }
}

resource "azurerm_cosmosdb_sql_role_assignment" "self" {
  name                = random_uuid.cosmosdb_role_assignment_guid_self.result
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  role_definition_id  = azurerm_cosmosdb_sql_role_definition.main.id
  principal_id        = data.azurerm_client_config.current.object_id
  scope               = azurerm_cosmosdb_account.main.id
}

resource "azurerm_cosmosdb_sql_role_assignment" "app" {
  name                = random_uuid.cosmosdb_role_assignment_guid_app.result
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  role_definition_id  = azurerm_cosmosdb_sql_role_definition.main.id
  principal_id        = azurerm_user_assigned_identity.main.principal_id
  scope               = azurerm_cosmosdb_account.main.id
}

resource "azurerm_cosmosdb_sql_role_assignment" "history_worker" {
  name                = random_uuid.cosmosdb_role_assignment_guid_history_worker.result
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  role_definition_id  = azurerm_cosmosdb_sql_role_definition.main.id
  principal_id        = azapi_resource.history_worker.output.identity.principalId
  scope               = azurerm_cosmosdb_account.main.id
}

resource "azurerm_cosmosdb_sql_role_assignment" "memory_api" {
  name                = random_uuid.cosmosdb_role_assignment_guid_memory_api.result
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  role_definition_id  = azurerm_cosmosdb_sql_role_definition.main.id
  principal_id        = azapi_resource.memory_api.output.identity.principalId
  scope               = azurerm_cosmosdb_account.main.id
}

resource "azurerm_cosmosdb_sql_role_assignment" "memory_worker" {
  name                = random_uuid.cosmosdb_role_assignment_guid_memory_worker.result
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  role_definition_id  = azurerm_cosmosdb_sql_role_definition.main.id
  principal_id        = azapi_resource.memory_worker.output.identity.principalId
  scope               = azurerm_cosmosdb_account.main.id
}

resource "azurerm_cosmosdb_sql_role_assignment" "history_api" {
  name                = random_uuid.cosmosdb_role_assignment_guid_history_api.result
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  role_definition_id  = azurerm_cosmosdb_sql_role_definition.main.id
  principal_id        = azapi_resource.history_api.output.identity.principalId
  scope               = azurerm_cosmosdb_account.main.id
}
