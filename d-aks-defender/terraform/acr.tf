resource "azurerm_container_registry" "main" {
  name                = random_string.main.result
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Premium"
  admin_enabled       = false
}

resource "azurerm_role_assignment" "acr" {
  scope                = azurerm_container_registry.main.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_user_assigned_identity.main.principal_id
}

resource "azapi_resource_action" "cve-2016-4977" {
  type                   = "Microsoft.ContainerRegistry/registries@2023-01-01-preview"
  resource_id            = azurerm_container_registry.main.id
  action                 = "importImage"
  body = <<EOF
{
  "source": {
    "registryUri": "registry.hub.docker.com",
    "sourceImage": "vulnerables/cve-2016-4977:latest"
  },
  "targetTags": [
    "vulnerables/cve-2016-4977:latest"
  ],
  "mode": "Force"
}
EOF
}

resource "azapi_resource_action" "cve-2016-7434" {
  type                   = "Microsoft.ContainerRegistry/registries@2023-01-01-preview"
  resource_id            = azurerm_container_registry.main.id
  action                 = "importImage"
  body = <<EOF
{
  "source": {
    "registryUri": "registry.hub.docker.com",
    "sourceImage": "vulnerables/cve-2016-7434:latest"
  },
  "targetTags": [
    "vulnerables/cve-2016-7434:latest"
  ],
  "mode": "Force"
}
EOF
}