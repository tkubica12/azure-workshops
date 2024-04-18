resource "azurerm_kusto_cluster" "main" {
  name                = module.main_naming.kusto_cluster.name_unique
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  sku {
    name     = "Standard_E2d_v4"
    capacity = 2
  }
}

resource "azurerm_kusto_database" "main" {
  name                = "sqlaudit"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  cluster_name        = azurerm_kusto_cluster.main.name
  hot_cache_period    = "P31D"
  soft_delete_period  = "P31D"
}

resource "azurerm_kusto_eventhub_data_connection" "main" {
  name                = "sqlaudit-connection"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  cluster_name        = azurerm_kusto_cluster.main.name
  database_name       = azurerm_kusto_database.main.name
  eventhub_id         = azurerm_eventhub.main.id
  consumer_group      = azurerm_eventhub_consumer_group.main.name

  #   table_name        = "my-table"         #(Optional)
  #   mapping_rule_name = "my-table-mapping" #(Optional)
  #   data_format       = "JSON"             #(Optional)
}
