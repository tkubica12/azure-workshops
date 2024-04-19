resource "azurerm_stream_analytics_job" "main" {
  name                                     = "sqlaudit-job"
  resource_group_name                      = azurerm_resource_group.main.name
  location                                 = azurerm_resource_group.main.location
  compatibility_level                      = "1.2"
  data_locale                              = "en-GB"
  events_late_arrival_max_delay_in_seconds = 60
  events_out_of_order_max_delay_in_seconds = 50
  events_out_of_order_policy               = "Adjust"
  output_error_policy                      = "Drop"
  streaming_units                          = 3
  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.main.id
    ]
  }

  transformation_query = <<EOF
SELECT
    ARRAYELEMENT.ArrayValue.resourceId AS resourceId,
    ARRAYELEMENT.ArrayValue.LogicalServerName AS LogicalServerName,
    ARRAYELEMENT.ArrayValue.ResourceGroup AS ResourceGroup,
    ARRAYELEMENT.ArrayValue.properties.audit_schema_version AS audit_schema_version,
    ARRAYELEMENT.ArrayValue.properties.event_time AS event_time,
    ARRAYELEMENT.ArrayValue.properties.sequence_number AS sequence_number,
    ARRAYELEMENT.ArrayValue.properties.action_id AS action_id,
    ARRAYELEMENT.ArrayValue.properties.action_name AS action_name,
    ARRAYELEMENT.ArrayValue.properties.succeeded AS succeeded,
    ARRAYELEMENT.ArrayValue.properties.is_column_permission AS is_column_permission,
    ARRAYELEMENT.ArrayValue.properties.session_id AS session_id,
    ARRAYELEMENT.ArrayValue.properties.server_principal_id AS server_principal_id,
    ARRAYELEMENT.ArrayValue.properties.database_principal_id AS database_principal_id,
    ARRAYELEMENT.ArrayValue.properties.target_server_principal_id AS target_server_principal_id,
    ARRAYELEMENT.ArrayValue.properties.target_database_principal_id AS target_database_principal_id,
    ARRAYELEMENT.ArrayValue.properties.object_id AS object_id,
    ARRAYELEMENT.ArrayValue.properties.user_defined_event_id AS user_defined_event_id,
    ARRAYELEMENT.ArrayValue.properties.transaction_id AS transaction_id,
    ARRAYELEMENT.ArrayValue.properties.class_type AS class_type,
    ARRAYELEMENT.ArrayValue.properties.class_type_description AS class_type_description,
    ARRAYELEMENT.ArrayValue.properties.securable_class_type AS securable_class_type,
    ARRAYELEMENT.ArrayValue.properties.duration_milliseconds AS duration_milliseconds,
    ARRAYELEMENT.ArrayValue.properties.response_rows AS response_rows,
    ARRAYELEMENT.ArrayValue.properties.affected_rows AS affected_rows,
    ARRAYELEMENT.ArrayValue.properties.client_tls_version AS client_tls_version,
    ARRAYELEMENT.ArrayValue.properties.database_transaction_id AS database_transaction_id,
    ARRAYELEMENT.ArrayValue.properties.ledger_start_sequence_number AS ledger_start_sequence_number,
    ARRAYELEMENT.ArrayValue.properties.is_local_secondary_replica AS is_local_secondary_replica,
    ARRAYELEMENT.ArrayValue.properties.client_ip AS client_ip,
    ARRAYELEMENT.ArrayValue.properties.permission_bitmask AS permission_bitmask,
    ARRAYELEMENT.ArrayValue.properties.sequence_group_id AS sequence_group_id,
    ARRAYELEMENT.ArrayValue.properties.session_server_principal_name AS session_server_principal_name,
    ARRAYELEMENT.ArrayValue.properties.server_principal_name AS server_principal_name,
    ARRAYELEMENT.ArrayValue.properties.server_principal_sid AS server_principal_sid,
    ARRAYELEMENT.ArrayValue.properties.database_principal_name AS database_principal_name,
    ARRAYELEMENT.ArrayValue.properties.target_server_principal_name AS target_server_principal_name,
    ARRAYELEMENT.ArrayValue.properties.target_server_principal_sid AS target_server_principal_sid,
    ARRAYELEMENT.ArrayValue.properties.target_database_principal_name AS target_database_principal_name,
    ARRAYELEMENT.ArrayValue.properties.server_instance_name AS server_instance_name,
    ARRAYELEMENT.ArrayValue.properties.database_name AS database_name,
    ARRAYELEMENT.ArrayValue.properties.schema_name AS schema_name,
    ARRAYELEMENT.ArrayValue.properties.object_name AS object_name,
    ARRAYELEMENT.ArrayValue.properties.statement AS statement,
    ARRAYELEMENT.ArrayValue.properties.additional_information AS additional_information,
    ARRAYELEMENT.ArrayValue.properties.user_defined_information AS user_defined_information,
    ARRAYELEMENT.ArrayValue.properties.application_name AS application_name,
    ARRAYELEMENT.ArrayValue.properties.connection_id AS connection_id,
    ARRAYELEMENT.ArrayValue.properties.data_sensitivity_information AS data_sensitivity_information,
    ARRAYELEMENT.ArrayValue.properties.host_name AS host_name,
    ARRAYELEMENT.ArrayValue.properties.session_context AS session_context,
    ARRAYELEMENT.ArrayValue.properties.client_tls_version_name AS client_tls_version_name,
    ARRAYELEMENT.ArrayValue.properties.external_policy_permissions_checked AS external_policy_permissions_checked,
    ARRAYELEMENT.ArrayValue.properties.obo_middle_tier_app_id AS obo_middle_tier_app_id,
    ARRAYELEMENT.ArrayValue.properties.is_server_level_audit AS is_server_level_audit,
    ARRAYELEMENT.ArrayValue.properties.event_id AS event_id
INTO
    adx
FROM
    sqlaudit
CROSS APPLY GetArrayElements(sqlaudit.records) AS ARRAYELEMENT
WHERE ARRAYELEMENT.ArrayValue.properties.action_id IS NOT NULL
EOF

}

resource "azurerm_stream_analytics_stream_input_eventhub_v2" "main" {
  name                         = "sqlaudit"
  stream_analytics_job_id      = azurerm_stream_analytics_job.main.id
  eventhub_consumer_group_name = azurerm_eventhub_consumer_group.main.name
  eventhub_name                = azurerm_eventhub.main.name
  servicebus_namespace         = azurerm_eventhub_namespace.main.name
  shared_access_policy_key     = azurerm_eventhub_namespace.main.default_primary_key
  shared_access_policy_name    = "RootManageSharedAccessKey"

  serialization {
    type     = "Json"
    encoding = "UTF8"
  }
}

resource "azapi_resource" "stream_adx_output" {
  type      = "Microsoft.StreamAnalytics/streamingjobs/outputs@2021-10-01-preview"
  name      = "adx"
  parent_id = azurerm_stream_analytics_job.main.id

  body = jsonencode({
    properties = {
      datasource = {
        type = "Microsoft.Kusto/clusters/databases"
        properties = {
          authenticationMode = "Msi"
          cluster            = azurerm_kusto_cluster.main.uri
          database           = azurerm_kusto_database.main.name
          table              = "sqlaudit"
        }
      }
      serialization = {
        type = "Json"
        properties = {
          encoding = "UTF8"
          format   = "LineSeparated"
        }
      }
      #   sizeWindow = int
      #   timeWindow = "string"
      #   watermarkSettings = {
      #     maxWatermarkDifferenceAcrossPartitions = "string"
      #     watermarkMode                          = "string"
      #   }
    }
  })
}
