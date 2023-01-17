resource "azurerm_resource_group" "main" {
  name     = "d-dedicated-hosts"
  location = var.location
}

resource "azapi_resource" "group_zone1" {
  type      = "Microsoft.Compute/hostGroups@2022-08-01"
  name      = "group-zone1"
  location  = azurerm_resource_group.main.location
  parent_id = azurerm_resource_group.main.id

  body = jsonencode({
    properties = {
      additionalCapabilities = {
        ultraSSDEnabled = false
      }
      platformFaultDomainCount  = 2
      supportAutomaticPlacement = true
    }
    zones = [
      "1"
    ]
  })
}

resource "azapi_resource" "group_zone2" {
  type      = "Microsoft.Compute/hostGroups@2022-08-01"
  name      = "group-zone2"
  location  = azurerm_resource_group.main.location
  parent_id = azurerm_resource_group.main.id

  body = jsonencode({
    properties = {
      additionalCapabilities = {
        ultraSSDEnabled = false
      }
      platformFaultDomainCount  = 2
      supportAutomaticPlacement = true
    }
    zones = [
      "2"
    ]
  })
}

resource "azapi_resource" "zone1_host1" {
  type      = "Microsoft.Compute/hostGroups/hosts@2022-08-01"
  name      = "zone1-host1"
  location  = azurerm_resource_group.main.location
  parent_id = azapi_resource.group_zone1.id

  body = jsonencode({
    properties = {
      autoReplaceOnFailure = true
      licenseType          = "None"
      platformFaultDomain  = 1
    }
    sku = {
      capacity = 1
      name     = var.sku
      tier     = "Standard"
    }
  })
}
