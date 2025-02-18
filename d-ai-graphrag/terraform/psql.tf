resource "azurerm_postgresql_flexible_server" "main" {
  name                          = "psql-${local.base_name}"
  resource_group_name           = azurerm_resource_group.main.name
  location                      = azurerm_resource_group.main.location
  version                       = "16"
  public_network_access_enabled = true
  storage_mb                    = 32768
  storage_tier                  = "P4"
  sku_name                      = "B_Standard_B1ms"

  authentication {
    active_directory_auth_enabled = true
    password_auth_enabled         = false
    tenant_id                     = data.azurerm_client_config.current.tenant_id
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.psql.id]
  }
}

