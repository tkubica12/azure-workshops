resource "azurerm_user_assigned_identity" "main" {
  name                = "uami-sql-audit"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_kusto_database_principal_assignment" "sql_audit_ingestor" {
  name                = "sql-audit-ingestor"
  resource_group_name = azurerm_resource_group.main.name
  cluster_name        = azurerm_kusto_cluster.main.name
  database_name       = azurerm_kusto_database.main.name

  tenant_id      = azurerm_user_assigned_identity.main.tenant_id
  principal_id   = azurerm_user_assigned_identity.main.principal_id
  principal_type = "App"
  role           = "Ingestor"
}

resource "azurerm_kusto_database_principal_assignment" "sql_audit_monitor" {
  name                = "sql-audit-monitor"
  resource_group_name = azurerm_resource_group.main.name
  cluster_name        = azurerm_kusto_cluster.main.name
  database_name       = azurerm_kusto_database.main.name

  tenant_id      = azurerm_user_assigned_identity.main.tenant_id
  principal_id   = azurerm_user_assigned_identity.main.principal_id
  principal_type = "App"
  role           = "Monitor"
}


