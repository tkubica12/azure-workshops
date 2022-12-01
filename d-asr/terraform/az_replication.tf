resource "azurerm_recovery_services_vault" "az" {
  name                = "az-replication-vault"
  location            = var.primary_location
  resource_group_name = azurerm_resource_group.az2.name
  sku                 = "Standard"
}

resource "azurerm_site_recovery_fabric" "az" {
  name                = "az-fabric"
  resource_group_name = azurerm_resource_group.az2.name
  recovery_vault_name = azurerm_recovery_services_vault.az.name
  location            = var.primary_location
}

# resource "azurerm_site_recovery_fabric" "secondary" {
#   name                = "secondary-fabric"
#   resource_group_name = azurerm_resource_group.secondary.name
#   recovery_vault_name = azurerm_recovery_services_vault.main.name
#   location            = azurerm_resource_group.secondary.location
#   depends_on          = [azurerm_site_recovery_fabric.primary]
# }

# resource "azurerm_site_recovery_network_mapping" "az" {
#   name                        = "az1-to-az2-network-mapping"
#   resource_group_name         = azurerm_resource_group.az2.name
#   recovery_vault_name         = azurerm_recovery_services_vault.az.name
#   source_recovery_fabric_name = azurerm_site_recovery_fabric.az.name
#   target_recovery_fabric_name = azurerm_site_recovery_fabric.az.name
#   source_network_id           = module.network_primary.spoke1_id
#   target_network_id           = module.network_primary.spoke1_id
# }

resource "azurerm_site_recovery_protection_container" "az1" {
  name                 = "az1-protection-container"
  resource_group_name  = azurerm_resource_group.az2.name
  recovery_vault_name  = azurerm_recovery_services_vault.az.name
  recovery_fabric_name = azurerm_site_recovery_fabric.az.name
}

resource "azurerm_site_recovery_protection_container" "az2" {
  name                 = "az2-protection-container"
  resource_group_name  = azurerm_resource_group.az2.name
  recovery_vault_name  = azurerm_recovery_services_vault.az.name
  recovery_fabric_name = azurerm_site_recovery_fabric.az.name
}

resource "azurerm_site_recovery_replication_policy" "az" {
  name                                                 = "policy"
  resource_group_name                                  = azurerm_resource_group.az2.name
  recovery_vault_name                                  = azurerm_recovery_services_vault.az.name
  recovery_point_retention_in_minutes                  = 180
  application_consistent_snapshot_frequency_in_minutes = 60
}

resource "azurerm_site_recovery_protection_container_mapping" "az" {
  name                                      = "az-container-mapping"
  resource_group_name                       = azurerm_resource_group.az2.name
  recovery_vault_name                       = azurerm_recovery_services_vault.az.name
  recovery_fabric_name                      = azurerm_site_recovery_fabric.az.name
  recovery_source_protection_container_name = azurerm_site_recovery_protection_container.az1.name
  recovery_target_protection_container_id   = azurerm_site_recovery_protection_container.az2.id
  recovery_replication_policy_id            = azurerm_site_recovery_replication_policy.az.id
}



