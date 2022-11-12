// Fleet Manager
resource "azapi_resource" "main" {
  type                      = "Microsoft.ContainerService/fleets@2022-09-02-preview"
  name                      = azurerm_resource_group.main.name
  location                  = local.reg1
  parent_id                 = azurerm_resource_group.main.id
  schema_validation_enabled = false

  body = jsonencode({
    properties = {
      hubProfile = {
        dnsPrefix = azurerm_resource_group.main.name
      }
    }
  })
}

// Get current client
data "azurerm_client_config" "current" {}

// Make current user Fleet cluster admin
resource "azurerm_role_assignment" "fleet" {
  principal_id         = data.azurerm_client_config.current.object_id
  role_definition_name = "Azure Kubernetes Fleet Manager RBAC Cluster Admin"
  scope                = azapi_resource.main.id
}

// Add cluster members
resource "azapi_resource" "fleet_member_reg1" {
  type                      = "Microsoft.ContainerService/fleets/members@2022-09-02-preview"
  name                      = "aks-${local.reg1}"
  parent_id                 = azapi_resource.main.id
  schema_validation_enabled = false

  body = jsonencode({
    properties = {
      clusterResourceId = azurerm_kubernetes_cluster.reg1.id
    }
  })
}

resource "azapi_resource" "fleet_member_reg2" {
  type                      = "Microsoft.ContainerService/fleets/members@2022-09-02-preview"
  name                      = "aks-${local.reg2}"
  parent_id                 = azapi_resource.main.id
  schema_validation_enabled = false

  body = jsonencode({
    properties = {
      clusterResourceId = azurerm_kubernetes_cluster.reg2.id
    }
  })
}
