data "azapi_resource" "default_gallery" {
  type      = "Microsoft.DevCenter/devcenters/galleries@2023-04-01"
  name      = "default"
  parent_id = azapi_resource.dev_center.id
}

data "azapi_resource" "default_image" {
  type      = "Microsoft.DevCenter/devcenters/galleries/images@2023-04-01"
  name      = var.devbox_image
  parent_id = data.azapi_resource.default_gallery.id
}

resource "azapi_resource" "devbox_definition" {
  type      = "Microsoft.DevCenter/devcenters/devboxdefinitions@2023-04-01"
  name      = "mydevbox"
  location  = azurerm_resource_group.main.location
  parent_id = azapi_resource.dev_center.id
  body = jsonencode({
    properties = {
      hibernateSupport = "Disabled"
      imageReference = {
        id = data.azapi_resource.default_image.id
      }
      sku = {
        name = var.devbox_size
      }
    }
  })
}

resource "azapi_resource" "network_connection" {
  type      = "Microsoft.DevCenter/networkConnections@2023-04-01"
  name      = "mynetwork_connection"
  location  = azurerm_resource_group.main.location
  parent_id = azurerm_resource_group.main.id
  body = jsonencode({
    properties = {
      domainJoinType              = "AzureADJoin"
      networkingResourceGroupName = local.dev_center_managed_network_rg
      subnetId                    = azurerm_subnet.main.id
    }
  })
}

resource "azapi_resource" "devcenter_attached_network" {
  type      = "Microsoft.DevCenter/devcenters/attachednetworks@2023-04-01"
  name      = "mynetwork"
  parent_id = azapi_resource.dev_center.id
  body = jsonencode({
    properties = {
      networkConnectionId = azapi_resource.network_connection.id
    }
  })
}

resource "azapi_resource" "devbox_pool" {
  type      = "Microsoft.DevCenter/projects/pools@2023-04-01"
  name      = "mypool"
  location  = azurerm_resource_group.main.location
  parent_id = azapi_resource.dev_project.id
  body = jsonencode({
    properties = {
      devBoxDefinitionName  = azapi_resource.devbox_definition.name
      licenseType           = "Windows_Client"
      localAdministrator    = "Enabled"
      networkConnectionName = azapi_resource.devcenter_attached_network.name
      stopOnDisconnect = {
        gracePeriodMinutes = 60
        status             = "Enabled"
      }
    }
  })
}

resource "azurerm_role_assignment" "devbox_user_self" {
  scope                = azapi_resource.dev_project.id
  role_definition_name = "DevCenter Dev Box User"
  principal_id         = data.azurerm_client_config.current.object_id
}
