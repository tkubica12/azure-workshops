resource "helm_release" "demo" {
  name       = "demo"
  chart      = "../helm"

  set {
    name  = "storage_access_client_id"
    value = azurerm_user_assigned_identity.storage_access.client_id
  }

  set {
    name  = "kv_access_client_id"
    value = azurerm_user_assigned_identity.kv_access.client_id
  }

  set {
    name  = "tenant_id"
    value = data.azurerm_client_config.current.tenant_id
  }

  set {
    name  = "kv_name"
    value = azurerm_key_vault.main.name
  }
}
