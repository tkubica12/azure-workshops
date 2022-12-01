resource "azurerm_recovery_services_vault" "main" {
  name                = "reg-replication-vault"
  location            = azurerm_resource_group.secondary.location
  resource_group_name = azurerm_resource_group.secondary.name
  sku                 = "Standard"
}

resource "azurerm_site_recovery_fabric" "primary" {
  name                = "primary-fabric"
  resource_group_name = azurerm_resource_group.secondary.name
  recovery_vault_name = azurerm_recovery_services_vault.main.name
  location            = var.primary_location
}

resource "azurerm_site_recovery_fabric" "secondary" {
  name                = "secondary-fabric"
  resource_group_name = azurerm_resource_group.secondary.name
  recovery_vault_name = azurerm_recovery_services_vault.main.name
  location            = azurerm_resource_group.secondary.location
  depends_on          = [azurerm_site_recovery_fabric.primary]
}

resource "azurerm_site_recovery_network_mapping" "main" {
  name                        = "primary-to-secondary-network-mapping"
  resource_group_name         = azurerm_resource_group.secondary.name
  recovery_vault_name         = azurerm_recovery_services_vault.main.name
  source_recovery_fabric_name = azurerm_site_recovery_fabric.primary.name
  target_recovery_fabric_name = azurerm_site_recovery_fabric.secondary.name
  source_network_id           = module.network_primary.spoke1_id
  target_network_id           = module.network_secondary.spoke1_id
}

resource "azurerm_site_recovery_protection_container" "primary" {
  name                 = "primary-protection-container"
  resource_group_name  = azurerm_resource_group.secondary.name
  recovery_vault_name  = azurerm_recovery_services_vault.main.name
  recovery_fabric_name = azurerm_site_recovery_fabric.primary.name
}

resource "azurerm_site_recovery_protection_container" "secondary" {
  name                 = "secondary-protection-container"
  resource_group_name  = azurerm_resource_group.secondary.name
  recovery_vault_name  = azurerm_recovery_services_vault.main.name
  recovery_fabric_name = azurerm_site_recovery_fabric.secondary.name
}

resource "azurerm_site_recovery_replication_policy" "main" {
  name                                                 = "policy"
  resource_group_name                                  = azurerm_resource_group.secondary.name
  recovery_vault_name                                  = azurerm_recovery_services_vault.main.name
  recovery_point_retention_in_minutes                  = 180
  application_consistent_snapshot_frequency_in_minutes = 60
}

resource "azurerm_site_recovery_protection_container_mapping" "main" {
  name                                      = "container-mapping"
  resource_group_name                       = azurerm_resource_group.secondary.name
  recovery_vault_name                       = azurerm_recovery_services_vault.main.name
  recovery_fabric_name                      = azurerm_site_recovery_fabric.primary.name
  recovery_source_protection_container_name = azurerm_site_recovery_protection_container.primary.name
  recovery_target_protection_container_id   = azurerm_site_recovery_protection_container.secondary.id
  recovery_replication_policy_id            = azurerm_site_recovery_replication_policy.main.id
}



