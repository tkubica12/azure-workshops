resource "azurerm_key_vault" "main" {
  name                      = module.naming.key_vault.name_unique
  resource_group_name       = var.resource_group_name
  location                  = var.location
  sku_name                  = "standard"
  enable_rbac_authorization = true
  tenant_id                 = data.azurerm_client_config.current.tenant_id
}

resource "azurerm_key_vault_secret" "storage_key" {
  name         = "storage-key"
  value        = azurerm_storage_account.main.primary_access_key
  key_vault_id = azurerm_key_vault.main.id

  depends_on = [
    azurerm_role_assignment.kv_self
  ]
}
