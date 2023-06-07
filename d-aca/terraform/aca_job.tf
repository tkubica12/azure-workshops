resource "azapi_resource" "job" {
  type                      = "Microsoft.App/jobs@2023-04-01-preview"
  schema_validation_enabled = false
  name                      = "job"
  location                  = azurerm_resource_group.main.location
  parent_id                 = azurerm_resource_group.main.id
  body = jsonencode({
    properties = {
      environmentId = azapi_resource.aca_ext_env.id
      configuration = {
        triggerType         = "Schedule"
        manualTriggerConfig = null
        registries          = null
        secrets             = null
        replicaTimeout      = 600
        replicaRetryLimit   = 5
        scheduleTriggerConfig = {
          replicaCompletionCount = 1
          parallelism            = 1
          cronExpression         = "*/5 * * * *"
        }
      }
      template = {
        containers = [
          {
            name  = "job"
            image = "mcr.microsoft.com/k8se/quickstart-jobs:latest"
            resources = {
              cpu    = 0.25
              memory = "0.5Gi"
            }
          }
        ]
        initContainers = null
        volumes        = null
      }
      workloadProfileName = "Consumption"
    }
  })

  lifecycle {
    ignore_changes = [
      schema_validation_enabled,
      type
    ]
  }
}
