# Virtual Machine in main region
resource "azurerm_network_interface" "main" {
  count               = var.vm_scenario ? 1 : 0
  name                = module.naming_main.network_interface.name
  location            = var.main_region
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.default_subnet_main.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_windows_virtual_machine" "main" {
  count               = var.vm_scenario ? 1 : 0
  name                = module.naming_main.virtual_machine.name
  location            = var.main_region
  resource_group_name = azurerm_resource_group.main.name
  size                = "Standard_B2ms"
  admin_username      = "tomas"
  admin_password      = random_string.password.result

  network_interface_ids = [
    azurerm_network_interface.main[0].id,
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "MicrosoftWindowsServer"
    offer     = "WindowsServer"
    sku       = "2019-Datacenter"
    version   = "latest"
  }
}

# Recovery services vault
resource "azurerm_recovery_services_vault" "main" {
  count                        = var.vm_scenario ? 1 : 0
  name                         = module.naming_main.recovery_services_vault.name_unique
  location                     = var.main_region
  resource_group_name          = azurerm_resource_group.main.name
  sku                          = "Standard"
  storage_mode_type            = "GeoRedundant"
  soft_delete_enabled          = false
  cross_region_restore_enabled = true
}

# Azure Backup policy
resource "azurerm_backup_policy_vm" "main" {
  count                          = var.vm_scenario ? 1 : 0
  name                           = "policy-${module.naming_main.recovery_services_vault.name}"
  resource_group_name            = azurerm_resource_group.main.name
  recovery_vault_name            = azurerm_recovery_services_vault.main[0].name
  instant_restore_retention_days = 2
  policy_type                    = "V2"
  timezone                       = "UTC"

  backup {
    frequency     = "Hourly"
    time          = "23:00"
    hour_interval = 4
    hour_duration = 12
  }

  retention_daily {
    count = 7
  }
}

# Enable Azure Backup on VM
resource "azurerm_backup_protected_vm" "main" {
  count               = var.vm_scenario ? 1 : 0
  resource_group_name = azurerm_resource_group.main.name
  recovery_vault_name = azurerm_recovery_services_vault.main[0].name
  source_vm_id        = azurerm_windows_virtual_machine.main[0].id
  backup_policy_id    = azurerm_backup_policy_vm.main[0].id
}

# Staging storage acccount in regions
module "storage_staging" {
  source = "Azure/naming/azurerm"
  suffix = [local.storage_region_short, "staging", "drdemo"]
}

resource "azurerm_storage_account" "storage_staging" {
  count                    = var.vm_scenario ? 1 : 0
  name                     = module.storage_staging.storage_account.name_unique
  resource_group_name      = azurerm_resource_group.main.name
  location                 = var.storage_region
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

module "main_staging" {
  source = "Azure/naming/azurerm"
  suffix = [local.main_region_short, "staging", "drdemo"]
}

resource "azurerm_storage_account" "main_staging" {
  count                    = var.vm_scenario ? 1 : 0
  name                     = module.main_staging.storage_account.name_unique
  resource_group_name      = azurerm_resource_group.main.name
  location                 = var.main_region
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Azure Site Recovery
resource "azurerm_recovery_services_vault" "target" {
  count                        = var.directreplication_scenario && var.vm_scenario ? 1 : 0
  name                         = module.naming_target.recovery_services_vault.name_unique
  location                     = var.target_region
  resource_group_name          = azurerm_resource_group.target.name
  sku                          = "Standard"
  storage_mode_type            = "GeoRedundant"
  soft_delete_enabled          = false
  cross_region_restore_enabled = true
}

resource "azurerm_site_recovery_fabric" "main" {
  count               = var.directreplication_scenario && var.vm_scenario ? 1 : 0
  name                = "primary-fabric"
  resource_group_name = azurerm_resource_group.target.name
  recovery_vault_name = azurerm_recovery_services_vault.target[0].name
  location            = var.main_region
}

resource "azurerm_site_recovery_fabric" "target" {
  count               = var.directreplication_scenario && var.vm_scenario ? 1 : 0
  name                = "secondary-fabric"
  resource_group_name = azurerm_resource_group.target.name
  recovery_vault_name = azurerm_recovery_services_vault.target[0].name
  location            = var.target_region
}

resource "azurerm_site_recovery_protection_container" "main" {
  count                = var.directreplication_scenario && var.vm_scenario ? 1 : 0
  name                 = "primary-protection-container"
  resource_group_name  = azurerm_resource_group.target.name
  recovery_vault_name  = azurerm_recovery_services_vault.target[0].name
  recovery_fabric_name = azurerm_site_recovery_fabric.main[0].name
}

resource "azurerm_site_recovery_protection_container" "target" {
  count                = var.directreplication_scenario && var.vm_scenario ? 1 : 0
  name                 = "secondary-protection-container"
  resource_group_name  = azurerm_resource_group.target.name
  recovery_vault_name  = azurerm_recovery_services_vault.target[0].name
  recovery_fabric_name = azurerm_site_recovery_fabric.target[0].name
}

resource "azurerm_site_recovery_replication_policy" "main" {
  count                                                = var.directreplication_scenario && var.vm_scenario ? 1 : 0
  name                                                 = "acr-policy"
  resource_group_name                                  = azurerm_resource_group.target.name
  recovery_vault_name                                  = azurerm_recovery_services_vault.target[0].name
  recovery_point_retention_in_minutes                  = 24 * 60
  application_consistent_snapshot_frequency_in_minutes = 60
}

resource "azurerm_site_recovery_protection_container_mapping" "main" {
  count                                     = var.directreplication_scenario && var.vm_scenario ? 1 : 0
  name                                      = "container-mapping"
  resource_group_name                       = azurerm_resource_group.target.name
  recovery_vault_name                       = azurerm_recovery_services_vault.target[0].name
  recovery_fabric_name                      = azurerm_site_recovery_fabric.main[0].name
  recovery_source_protection_container_name = azurerm_site_recovery_protection_container.main[0].name
  recovery_target_protection_container_id   = azurerm_site_recovery_protection_container.target[0].id
  recovery_replication_policy_id            = azurerm_site_recovery_replication_policy.main[0].id
}

resource "azurerm_site_recovery_network_mapping" "main" {
  count                       = var.directreplication_scenario && var.vm_scenario ? 1 : 0
  name                        = "network-mapping"
  resource_group_name         = azurerm_resource_group.target.name
  recovery_vault_name         = azurerm_recovery_services_vault.target[0].name
  source_recovery_fabric_name = azurerm_site_recovery_fabric.main[0].name
  target_recovery_fabric_name = azurerm_site_recovery_fabric.target[0].name
  source_network_id           = azurerm_virtual_network.vnet_main.id
  target_network_id           = azurerm_virtual_network.vnet_target.id
}

data "azurerm_managed_disk" "os_disk" {
  name                = azurerm_windows_virtual_machine.main[0].os_disk[0].name
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_site_recovery_replicated_vm" "main" {
  count                                     = var.directreplication_scenario && var.vm_scenario ? 1 : 0
  name                                      = "vm-replication"
  resource_group_name                       = azurerm_resource_group.target.name
  recovery_vault_name                       = azurerm_recovery_services_vault.target[0].name
  source_recovery_fabric_name               = azurerm_site_recovery_fabric.main[0].name
  source_vm_id                              = azurerm_windows_virtual_machine.main[0].id
  recovery_replication_policy_id            = azurerm_site_recovery_replication_policy.main[0].id
  source_recovery_protection_container_name = azurerm_site_recovery_protection_container.main[0].name
  target_resource_group_id                  = azurerm_resource_group.target.id
  target_recovery_fabric_id                 = azurerm_site_recovery_fabric.target[0].id
  target_recovery_protection_container_id   = azurerm_site_recovery_protection_container.target[0].id

  managed_disk {
    disk_id                    = data.azurerm_managed_disk.os_disk.id
    staging_storage_account_id = azurerm_storage_account.main_staging[0].id
    target_resource_group_id   = azurerm_resource_group.main.id
    target_disk_type           = "Standard_LRS"
    target_replica_disk_type   = "Standard_LRS"
  }

  network_interface {
    source_network_interface_id = azurerm_network_interface.main[0].id
    target_subnet_name          = azurerm_subnet.default_subnet_target.name
  }

  depends_on = [
    azurerm_site_recovery_protection_container_mapping.main,
    azurerm_site_recovery_network_mapping.main,
  ]
}
