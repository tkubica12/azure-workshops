resource "azurerm_kubernetes_cluster" "main" {
  name                      = "d-aks-federated-identity"
  location                  = azurerm_resource_group.main.location
  resource_group_name       = azurerm_resource_group.main.name
  dns_prefix                = "d-aks-federated-identity"
  workload_identity_enabled = true
  oidc_issuer_enabled       = true

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_B2ms"
  }

  identity {
    type = "SystemAssigned"
  }

  key_vault_secrets_provider {
    secret_rotation_enabled = true
  }
}
