resource "azurerm_key_vault" "main" {
  name                          = "kv${random_string.main.result}"
  resource_group_name           = var.resource_group_name
  location                      = var.location
  tenant_id                     = data.azurerm_client_config.current.tenant_id
  sku_name                      = "standard"
  purge_protection_enabled      = false
  enable_rbac_authorization     = true
  soft_delete_retention_days    = 7
  public_network_access_enabled = false
}

resource "azurerm_private_endpoint" "kv" {
  name                = "kv-endpoint"
  resource_group_name = var.resource_group_name
  location            = var.location
  subnet_id           = var.subnet_id_kv

  private_dns_zone_group {
    name                 = "kv-dns"
    private_dns_zone_ids = [var.privatedns_id]
  }

  private_service_connection {
    name                           = "kv-connection"
    is_manual_connection           = false
    private_connection_resource_id = azurerm_key_vault.main.id
    subresource_names              = ["vault"]
  }
}

resource "azurerm_role_assignment" "kv_self" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Administrator"
  principal_id         = data.azurerm_client_config.current.object_id
}


resource "azurerm_key_vault_certificate" "main" {
  name         = "cert"
  key_vault_id = var.keyvault_id

  certificate {
    contents = filebase64("${path.module}/../certs/server.pfx")
    password = "Azure12345678"
  }

  depends_on = [
    azurerm_role_assignment.kv_self,
    azurerm_role_assignment.kv_appgw,
    azurerm_private_endpoint.kv
  ]
}

