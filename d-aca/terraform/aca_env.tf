resource "azapi_resource" "aca_int_env" {
  type      = "Microsoft.App/managedEnvironments@2022-11-01-preview"
  name      = "d-aca-int-env"
  location  = azurerm_resource_group.main.location
  parent_id = azurerm_resource_group.main.id
  body = jsonencode({
    properties = {
      appLogsConfiguration = {
        destination = "log-analytics"
        logAnalyticsConfiguration = {
          customerId = azurerm_log_analytics_workspace.main.workspace_id
          sharedKey  = azurerm_log_analytics_workspace.main.primary_shared_key
        }
      }
      infrastructureResourceGroup = "d-aca-int-env-infra"
      vnetConfiguration = {
        infrastructureSubnetId = azurerm_subnet.aca_int.id
        internal               = true
      }
      workloadProfiles = [
        {
          name                = "Consumption"
          workloadProfileType = "Consumption"
        },
        {
          name                = "myprofile"
          workloadProfileType = "D4"
          maximumCount        = 1
          minimumCount        = 0
        }
      ]
      zoneRedundant = false
    }
  })
}

resource "azapi_resource" "aca_ext_env" {
  type      = "Microsoft.App/managedEnvironments@2022-11-01-preview"
  name      = "d-aca-ext-env"
  location  = azurerm_resource_group.main.location
  parent_id = azurerm_resource_group.main.id
  body = jsonencode({
    properties = {
      appLogsConfiguration = {
        destination = "log-analytics"
        logAnalyticsConfiguration = {
          customerId = azurerm_log_analytics_workspace.main.workspace_id
          sharedKey  = azurerm_log_analytics_workspace.main.primary_shared_key
        }
      }
      infrastructureResourceGroup = "d-aca-ext-env-infra"
      vnetConfiguration = {
        infrastructureSubnetId = azurerm_subnet.aca_ext.id
        internal               = false
      }
      workloadProfiles = [
        {
          name                = "Consumption"
          workloadProfileType = "Consumption"
        },
        {
          name                = "myprofile"
          workloadProfileType = "D4"
          maximumCount        = 1
          minimumCount        = 0
        }
      ]
      zoneRedundant = false
    }
  })
}

resource "azapi_resource" "storage_env_mapping" {
  type      = "Microsoft.App/managedEnvironments/storages@2022-11-01-preview"
  name      = "myfiles"
  parent_id = azapi_resource.aca_ext_env.id
  body = jsonencode({
    properties = {
      azureFile = {
        accessMode  = "ReadOnly"
        accountKey  = azurerm_storage_account.files.primary_access_key
        accountName = azurerm_storage_account.files.name
        shareName   = azurerm_storage_share.main.name
      }
    }
  })
}
