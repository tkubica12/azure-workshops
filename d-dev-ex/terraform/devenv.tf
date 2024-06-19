resource "azapi_resource" "main" {
  type      = "Microsoft.DevCenter/devcenters/catalogs@2023-04-01"
  name      = "mycatalog"
  parent_id = azapi_resource.dev_center.id
  body = jsonencode({
    properties = {
      gitHub = {
        branch = "main"
        path   = "Environment-Definitions"
        uri    = "https://github.com/microsoft/devcenter-catalog.git"
      }
    }
  })
}

resource "azapi_resource" "env_type" {
  type      = "Microsoft.DevCenter/devcenters/environmentTypes@2023-04-01"
  name      = "CompanyEnvironmentType"
  parent_id = azapi_resource.dev_center.id
  body = jsonencode({
    properties = {}
  })
}

resource "azapi_resource" "env_type_assignment" {
  type      = "Microsoft.DevCenter/projects/environmentTypes@2023-04-01"
  name      = "CompanyEnvironmentType"
  location  = azurerm_resource_group.main.location
  parent_id = azapi_resource.dev_project.id

  identity {
    type = "SystemAssigned"
  }

  body = jsonencode({
    properties = {
      creatorRoleAssignment = {
        roles = {
          "acdd72a7-3385-48ef-bd42-f606fba81ae7" = {} // Reader
        }
      }
      status             = "Enabled"
      deploymentTargetId = "/subscriptions/${data.azurerm_client_config.current.subscription_id}"
    }
  })
}

resource "azurerm_role_assignment" "devenv_self" {
  scope                = azapi_resource.dev_project.id
  role_definition_name = "Deployment Environments User"
  principal_id         = data.azurerm_client_config.current.object_id
}


