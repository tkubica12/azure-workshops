// Primary location cache
resource "azurerm_storage_account" "asr" {
  name                     = "asr${random_string.main.result}"
  location                 = var.primary_location
  resource_group_name      = azurerm_resource_group.primary.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

// Access from primary location VM via Private Endpoint
resource "azurerm_private_endpoint" "asr" {
  name                = "asr-cache-endpoint"
  location            = var.primary_location
  resource_group_name = azurerm_resource_group.primary.name
  subnet_id           = module.network_primary.spoke1_subnet1_id

  private_dns_zone_group {
    name                 = "zgroup"
    private_dns_zone_ids = [azurerm_private_dns_zone.storage.id]
  }

  private_service_connection {
    name                           = "asr-privateserviceconnection"
    private_connection_resource_id = azurerm_storage_account.asr.id
    subresource_names              = ["blob"]
    is_manual_connection           = false
  }
}

// Secondary location cache (just to be there for reprotect aka fail-back)
resource "azurerm_storage_account" "asr_secondary" {
  name                     = "asrsec${random_string.main.result}"
  location                 = var.secondary_location
  resource_group_name      = azurerm_resource_group.secondary.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

// Access from secondary location VM via Private Endpoint (just to be there for reprotect aka fail-back)
resource "azurerm_private_endpoint" "asr_secondary" {
  name                = "asrsec-cache-endpoint"
  location            = var.secondary_location
  resource_group_name = azurerm_resource_group.secondary.name
  subnet_id           = module.network_secondary.spoke1_subnet1_id

  private_dns_zone_group {
    name                 = "zgroup"
    private_dns_zone_ids = [azurerm_private_dns_zone.storage.id]
  }

  private_service_connection {
    name                           = "asrsec-privateserviceconnection"
    private_connection_resource_id = azurerm_storage_account.asr_secondary.id
    subresource_names              = ["blob"]
    is_manual_connection           = false
  }
}

// PaaS access by ASR
# resource "azurerm_storage_account_network_rules" "asr" {
#   storage_account_id = azurerm_storage_account.asr.id
#   default_action     = "Deny"
#   bypass             = ["AzureServices"]

#   private_link_access {
#     endpoint_resource_id = azurerm_recovery_services_vault.main.id
#   }

#   depends_on = [
#     azurerm_recovery_services_vault.main
#   ]
# }
