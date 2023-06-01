resource "azapi_resource" "web_ext" {
  type      = "Microsoft.App/containerapps@2022-11-01-preview"
  name      = "web-ext"
  location  = azurerm_resource_group.main.location
  parent_id = azurerm_resource_group.main.id
  body = jsonencode({
    properties = {
      environmentId = azapi_resource.aca_ext_env.id
      configuration = {
        activeRevisionsMode = "Single"
        ingress = {
          external   = true
          targetPort = 80
        }
      }
      template = {
        scale = {
          minReplicas = 1
        }
        containers = [
          {
            name  = "simple-hello-world-container"
            image = "mcr.microsoft.com/k8se/quickstart:latest"
            resources = {
              cpu    = 0.25
              memory = "0.5Gi"
            }
          }
        ]
      }
      workloadProfileName = "Consumption"
    }
  })
}

resource "azapi_resource" "web_int" {
  type      = "Microsoft.App/containerapps@2022-11-01-preview"
  name      = "web-int"
  location  = azurerm_resource_group.main.location
  parent_id = azurerm_resource_group.main.id
  body = jsonencode({
    properties = {
      environmentId = azapi_resource.aca_int_env.id
      configuration = {
        activeRevisionsMode = "Single"
        ingress = {
          external   = true
          targetPort = 80
        }
      }
      template = {
        scale = {
          minReplicas = 1
        }
        containers = [
          {
            name  = "simple-hello-world-container"
            image = "mcr.microsoft.com/k8se/quickstart:latest"
            resources = {
              cpu    = 0.25
              memory = "0.5Gi"
            }
          }
        ]
      }
      workloadProfileName = "Consumption"
    }
  })
}
