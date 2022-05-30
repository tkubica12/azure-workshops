// Generate random name
resource "random_string" "name" {
  length  = 12
  special = false
  upper   = false
  lower   = true
  number  = false
}

// Generate random password
resource "random_password" "password" {
  length           = 16
  special          = true
  override_special = "!#,"
  min_special      = 1
  lower            = true
  min_lower        = 1
  upper            = true
  min_upper        = 1
  number           = true
  min_numeric      = 1
}

// SQL server
resource "azurerm_mssql_server" "module" {
  name                         = "${var.prefix}-${random_string.name.result}"
  resource_group_name          = var.resourceGroupName
  location                     = var.location
  version                      = "12.0"
  administrator_login          = "azureuser"
  administrator_login_password = random_password.password.result
}

// Store password to Key Vault
resource "azurerm_key_vault_secret" "sqlpassword" {
  name         = "${var.prefix}-${random_string.name.result}"
  value        = random_password.password.result
  key_vault_id = var.keyVaultId
}

// Create Private Endpoint and DNS zone group
resource "azurerm_private_endpoint" "azuresql" {
  name                = "${azurerm_mssql_server.module.name}-pe"
  resource_group_name = var.resourceGroupName
  location            = var.location
  subnet_id           = var.subnetId

  private_dns_zone_group {
    name                 = "${azurerm_mssql_server.module.name}-zonegroup"
    private_dns_zone_ids = [var.dnsZoneId]
  }

  private_service_connection {
    name                           = "${azurerm_mssql_server.module.name}-pconnection"
    private_connection_resource_id = azurerm_mssql_server.module.id
    is_manual_connection           = false
    subresource_names              = ["sqlServer"]
  }
}

// SQL Database
resource "azurerm_mssql_database" "module" {
  name           = var.dbName
  server_id      = azurerm_mssql_server.module.id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  read_scale     = var.readScale
  sku_name       = var.skuName
  zone_redundant = var.zoneRedundant
}
