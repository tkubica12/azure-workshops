# Module for creating a unique name for the ZRS storage account
module "storage_main_zrs" {
  source = "Azure/naming/azurerm"
  suffix = [local.main_region_short, "zrs", "drdemo"]
}

# ZRS Storage Account Resource
resource "azurerm_storage_account" "storage_main_zrs" {
  count                    = var.directreplication_scenario && var.storage_scenario ? 1 : 0
  name                     = module.storage_main_zrs.storage_account.name_unique
  resource_group_name      = azurerm_resource_group.main.name
  location                 = var.main_region
  account_tier             = "Standard"
  account_replication_type = "ZRS"

  blob_properties {
    versioning_enabled  = true
    change_feed_enabled = true
  }
}

# Storage container and blob
resource "azurerm_storage_container" "storage_main_zrs" {
  count                 = var.directreplication_scenario && var.storage_scenario ? 1 : 0
  name                  = "mycontainer"
  storage_account_name  = azurerm_storage_account.storage_main_zrs[0].name
  container_access_type = "private"
}

resource "azurerm_storage_blob" "storage_main_zrs" {
  count                  = var.directreplication_scenario && var.storage_scenario ? 1 : 0
  name                   = "greatfile.txt"
  storage_account_name   = azurerm_storage_account.storage_main_zrs[0].name
  storage_container_name = azurerm_storage_container.storage_main_zrs[0].name
  type                   = "Block"
  source_content         = "My fantastic data"

  depends_on = [azurerm_storage_object_replication.object_replication]
}


# Module for creating a unique name for the GRS storage account
module "storage_main_grs" {
  source = "Azure/naming/azurerm"
  suffix = [local.main_region_short, "grs", "drdemo"]
}

# GRS Storage Account Resource
resource "azurerm_storage_account" "storage_main_grs" {
  count                    = var.indirectreplication_scenario && var.storage_scenario ? 1 : 0
  name                     = module.storage_main_grs.storage_account.name_unique
  resource_group_name      = azurerm_resource_group.main.name
  location                 = var.main_region
  account_tier             = "Standard"
  account_replication_type = "GZRS"
}

# Storage container and blob
resource "azurerm_storage_container" "storage_main_grs" {
  count                 = var.indirectreplication_scenario && var.storage_scenario ? 1 : 0
  name                  = "mycontainer"
  storage_account_name  = azurerm_storage_account.storage_main_grs[0].name
  container_access_type = "private"
}

resource "azurerm_storage_blob" "storage_main_grs" {
  count                  = var.indirectreplication_scenario && var.storage_scenario ? 1 : 0
  name                   = "greatfile.txt"
  storage_account_name   = azurerm_storage_account.storage_main_grs[0].name
  storage_container_name = azurerm_storage_container.storage_main_grs[0].name
  type                   = "Block"
  source_content         = "My fantastic data"
}

# Module for creating a unique name for the LRS storage account
module "storage_target_lrs" {
  source = "Azure/naming/azurerm"
  suffix = [local.target_region_short, "lrs", "drdemo"]
}

# LRS Storage Account Resource
resource "azurerm_storage_account" "storage_target_lrs" {
  count                    = var.directreplication_scenario && var.storage_scenario ? 1 : 0
  name                     = module.storage_target_lrs.storage_account.name_unique
  resource_group_name      = azurerm_resource_group.target.name
  location                 = var.target_region
  account_tier             = "Standard"
  account_replication_type = "LRS"

  blob_properties {
    versioning_enabled  = true
    change_feed_enabled = true
  }
}

# Storage container
resource "azurerm_storage_container" "storage_target_lrs" {
  count                 = var.directreplication_scenario && var.storage_scenario ? 1 : 0
  name                  = "mycontainer"
  storage_account_name  = azurerm_storage_account.storage_target_lrs[0].name
  container_access_type = "private"
}

# Object replication
resource "azurerm_storage_object_replication" "object_replication" {
  count                          = var.directreplication_scenario && var.storage_scenario ? 1 : 0
  source_storage_account_id      = azurerm_storage_account.storage_main_zrs[0].id
  destination_storage_account_id = azurerm_storage_account.storage_target_lrs[0].id

  rules {
    source_container_name      = azurerm_storage_container.storage_main_zrs[0].name
    destination_container_name = azurerm_storage_container.storage_target_lrs[0].name
  }
}
