resource "azurerm_storage_account" "main" {
  name                     = random_string.main.result
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_queue" "main" {
  name                 = "myqueue"
  storage_account_name = azurerm_storage_account.main.name
}

resource "azapi_resource" "function" {
  type                      = "Microsoft.Web/sites@2022-03-01"
  schema_validation_enabled = false
  name                      = random_string.main.result
  location                  = azurerm_resource_group.main.location
  parent_id                 = azurerm_resource_group.main.id
  body = jsonencode({
    kind = "functionapp,linux,container,azurecontainerapps"
    properties = {
      name                 = random_string.main.result
      managedEnvironmentId = azapi_resource.aca_ext_env.id
      siteConfig = {
        linuxFxVersion = "DOCKER|ghcr.io/tkubica12/azure_function:latest"
        appSettings = [
          {
            name  = "AzureWebJobsStorage"
            value = "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=${azurerm_storage_account.main.name};AccountKey=${azurerm_storage_account.main.primary_access_key}"
          },
          {
            name  = "DOCKER_REGISTRY_SERVER_URL"
            value = "ghcr.io"
          },
          {
            name  = "queueConnectionString"
            value = "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=${azurerm_storage_account.main.name};AccountKey=${azurerm_storage_account.main.primary_access_key}"
          }
        ]
      }
    }
  })
  depends_on = [azurerm_storage_queue.main]
}
