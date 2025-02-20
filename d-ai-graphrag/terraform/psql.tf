// Azure PostgreSQL Flexible Server
resource "random_password" "psql" {
  length  = 16
  special = true
}

resource "azurerm_postgresql_flexible_server" "main" {
  name                          = "psql-${local.base_name}"
  resource_group_name           = azurerm_resource_group.main.name
  location                      = azurerm_resource_group.main.location
  version                       = "16"
  public_network_access_enabled = true
  storage_mb                    = 32768
  storage_tier                  = "P4"
  sku_name                      = "B_Standard_B1ms"
  administrator_login           = "psqladmin"
  administrator_password        = random_password.psql.result

  authentication {
    active_directory_auth_enabled = true
    password_auth_enabled         = true
    tenant_id                     = data.azurerm_client_config.current.tenant_id
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.psql.id]
  }

  lifecycle {
    ignore_changes = [high_availability, zone]
  }
}

// PostgreSQL Flexible Server Database
resource "azurerm_postgresql_flexible_server_database" "demo" {
  name      = "demo"
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

// PostgreSQL Flexible Server Firewall Rule
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_all" {
  name             = "allow-all-fw"
  server_id        = azurerm_postgresql_flexible_server.main.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "255.255.255.255"
}

// PostgreSQL Flexible Server Configuration
resource "azurerm_postgresql_flexible_server_configuration" "main" {
  name      = "azure.extensions"
  server_id = azurerm_postgresql_flexible_server.main.id
  value     = "vector,pg_diskann,azure_ai"
}

// Outputs
output "PGHOST" {
  value = azurerm_postgresql_flexible_server.main.fqdn
}

output "PGDATABASE" {
  value = azurerm_postgresql_flexible_server_database.demo.name
}

output "PGPASSWORD" {
  value     = random_password.psql.result
  sensitive = true
}

output "PGUSER" {
  value = azurerm_postgresql_flexible_server.main.administrator_login
}
