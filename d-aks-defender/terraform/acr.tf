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

resource "azapi_resource_action" "import" {
  type                   = "Microsoft.ContainerRegistry/registries@2023-01-01-preview"
  resource_id            = azurerm_container_registry.main.id
  action                 = "importImage"
  body = <<EOF
{
  "source": {
    "registryUri": "registry.hub.docker.com",
    "sourceImage": "library/ubuntu:13.10"
  },
  "targetTags": [
    "ubuntu:13.10"
  ],
  "mode": "Force"
}
EOF
}