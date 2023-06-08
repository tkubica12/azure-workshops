resource "azapi_resource" "web_ext" {
  type      = "Microsoft.App/containerapps@2022-11-01-preview"
  name      = "web-ext"
  location  = azurerm_resource_group.main.location
  parent_id = azurerm_resource_group.main.id
  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.kv_reader.id
    ]
  }
  body = jsonencode({
    properties = {
      environmentId = azapi_resource.aca_ext_env.id
      configuration = {
        activeRevisionsMode = "Single"
        ingress = {
          external   = true
          targetPort = 80
        }
        secrets = [
          {
            identity    = azurerm_user_assigned_identity.kv_reader.id
            keyVaultUrl = azurerm_key_vault_secret.main.id
            name        = "mysecret"
          }
        ]
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
            volumeMounts = [
              {
                volumeName = "myfiles"
                mountPath  = "/myfiles"
              }
            ]
            env = [
              {
                name      = "mysecret"
                secretRef = "mysecret"
              }
            ]
          }
        ]
        initContainers = [
          {
            name  = "init-container"
            image = "ubuntu:latest"
            command = [
              "/bin/bash",
              "-c",
              "sleep 1"
            ]
            resources = {
              cpu    = 0.25
              memory = "0.5Gi"
            }
          }
        ]
        volumes = [
          {
            name        = "myfiles"
            storageName = "myfiles"
            storageType = "AzureFile"
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
