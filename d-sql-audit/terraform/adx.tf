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

resource "azurerm_kusto_script" "createtable" {
  name           = "createtable"
  database_id    = azurerm_kusto_database.main.id
  script_content = <<EOF
.create table sqlaudit (
    resourceId: string,
    LogicalServerName: string,
    ResourceGroup: string,
    audit_schema_version: int,
    event_time: datetime,
    sequence_number: long,
    action_id: string,
    action_name: string,
    succeeded: bool,
    is_column_permission: bool,
    session_id: int,
    server_principal_id: int,
    database_principal_id: int,
    target_server_principal_id: int,
    target_database_principal_id: int,
    object_id: int,
    user_defined_event_id: int,
    transaction_id: long,
    class_type: string,
    class_type_description: string,
    securable_class_type: string,
    duration_milliseconds: int,
    response_rows: int,
    affected_rows: int,
    client_tls_version: int,
    database_transaction_id: long,
    ledger_start_sequence_number: long,
    is_local_secondary_replica: bool,
    client_ip: string,
    permission_bitmask: string,
    sequence_group_id: string,
    session_server_principal_name: string,
    server_principal_name: string,
    server_principal_sid: string,
    database_principal_name: string,
    target_server_principal_name: string,
    target_server_principal_sid: string,
    target_database_principal_name: string,
    server_instance_name: string,
    database_name: string,
    schema_name: string,
    object_name: string,
    statement: string,
    additional_information: string,
    user_defined_information: string,
    application_name: string,
    connection_id: string,
    data_sensitivity_information: string,
    host_name: string,
    session_context: string,
    client_tls_version_name: string,
    external_policy_permissions_checked: string,
    obo_middle_tier_app_id: string,
    is_server_level_audit: bool,
    event_id: string
)
EOF
}

# resource "azurerm_kusto_eventhub_data_connection" "main" {
#   name                = "sqlaudit-connection"
#   resource_group_name = azurerm_resource_group.main.name
#   location            = azurerm_resource_group.main.location
#   cluster_name        = azurerm_kusto_cluster.main.name
#   database_name       = azurerm_kusto_database.main.name
#   eventhub_id         = azurerm_eventhub.main.id
#   consumer_group      = azurerm_eventhub_consumer_group.main.name
#   # table_name          = "sqlaudit" #(Optional)
#   # mapping_rule_name = "my-table-mapping" #(Optional)
#   data_format = "AVRO" #(Optional)
# }
