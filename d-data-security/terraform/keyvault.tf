# resource "azurerm_key_vault_managed_hardware_security_module" "main" {
#   name                       = "${random_string.main.result}hsm"
#   resource_group_name        = azurerm_resource_group.main.name
#   location                   = azurerm_resource_group.main.location
#   sku_name                   = "Standard_B1"
#   purge_protection_enabled   = false
#   soft_delete_retention_days = 7
#   tenant_id                  = data.azurerm_client_config.current.tenant_id
#   admin_object_ids           = [data.azurerm_client_config.current.object_id]
# }

resource "azurerm_key_vault" "main" {
  name                        = "${random_string.main.result}kv"
  location                    = azurerm_resource_group.main.location
  resource_group_name         = azurerm_resource_group.main.name
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "premium"
  enable_rbac_authorization   = true
  enabled_for_disk_encryption = true
  purge_protection_enabled    = true
  soft_delete_retention_days  = 7
}

resource "azurerm_role_assignment" "kv_main" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Administrator"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_key_vault_key" "main" {
  name         = "key-encryption"
  key_vault_id = azurerm_key_vault.main.id
  key_type     = "RSA"
  key_size     = 2048
  key_opts     = ["decrypt", "encrypt", "sign", "unwrapKey", "verify", "wrapKey"]

  depends_on = [
    azurerm_role_assignment.kv_main
  ]
}

