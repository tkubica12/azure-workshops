resource "azurerm_container_app_environment" "main" {
  name                       = "cae-${local.base_name}"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
}

# resource "azapi_resource" "container_app_environment" {
#   type      = "Microsoft.App/managedEnvironments@2024-10-02-preview"
#   name      = "cae-${local.base_name}"
#   location  = azurerm_resource_group.main.location
#   parent_id = azurerm_resource_group.main.id
#   schema_validation_enabled = false

#   body = {
#     properties = {
#       appLogsConfiguration = {
#         destination = "log-analytics",
#         logAnalyticsConfiguration = {
#           customerId = azurerm_log_analytics_workspace.main.workspace_id,
#           sharedKey  = azurerm_log_analytics_workspace.main.primary_shared_key
#         }
#       }
#       appInsightsConfiguration = {
#         connectionString = azurerm_application_insights.main.connection_string
#       }
#       openTelemetryConfiguration = {
#         tracesConfiguration = {
#           destinations = ["appInsights"]
#         }
#         logsConfiguration = {
#           destinations = ["appInsights"]
#         }
#       }
#     }
#   }
# }
