module "naming" {
  source = "Azure/naming/azurerm"
  suffix = ["drdemo"]
}

resource "azurerm_resource_group" "main" {
  name     = module.naming.resource_group.name
  location = var.main_region
}

resource "azurerm_resource_group" "target" {
  name     = "${module.naming.resource_group.name}-target"
  location = var.target_region
}

resource "random_string" "password" {
  upper   = true
  length  = 16
  lower   = true
  numeric = true
  special = true
}

resource "azurerm_private_dns_zone" "dns" {
  count               = var.psql_scenario ? 1 : 0
  name                = "demo.postgres.database.azure.com"
  resource_group_name = azurerm_resource_group.main.name
}

# Base resources in main region
module "naming_main" {
  source = "Azure/naming/azurerm"
  suffix = [local.main_region_short, "drdemo"]
}

resource "azurerm_virtual_network" "vnet_main" {
  name                = module.naming_main.virtual_network.name
  location            = var.main_region
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "default_subnet_main" {
  name                 = "default"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.vnet_main.name
  address_prefixes     = ["10.0.0.0/24"]
}

resource "azurerm_subnet" "psql_subnet_main" {
  count                = var.psql_scenario ? 1 : 0
  name                 = "psql"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.vnet_main.name
  address_prefixes     = ["10.0.1.0/24"]

  delegation {
    name = "psql"
    service_delegation {
      name = "Microsoft.DBforPostgreSQL/flexibleServers"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
      ]
    }
  }
}

resource "azurerm_private_dns_zone_virtual_network_link" "dns_main" {
  count                 = var.psql_scenario ? 1 : 0
  name                  = module.naming_main.virtual_network.name_unique
  private_dns_zone_name = azurerm_private_dns_zone.dns[0].name
  virtual_network_id    = azurerm_virtual_network.vnet_main.id
  resource_group_name   = azurerm_resource_group.main.name

  depends_on = [
    azurerm_subnet.psql_subnet_main,
    azurerm_subnet.psql_subnet_target
  ]
}

# Base resources in target region
module "naming_target" {
  source = "Azure/naming/azurerm"
  suffix = [local.target_region_short, "drdemo"]
}

resource "azurerm_virtual_network" "vnet_target" {
  name                = module.naming_target.virtual_network.name
  location            = var.target_region
  resource_group_name = azurerm_resource_group.target.name
  address_space       = ["10.1.0.0/16"]
}

resource "azurerm_virtual_network_peering" "main2target" {
  name                      = "main2target"
  resource_group_name       = azurerm_resource_group.main.name
  virtual_network_name      = azurerm_virtual_network.vnet_main.name
  remote_virtual_network_id = azurerm_virtual_network.vnet_target.id
}

resource "azurerm_virtual_network_peering" "target1main" {
  name                      = "target2main"
  resource_group_name       = azurerm_resource_group.target.name
  virtual_network_name      = azurerm_virtual_network.vnet_target.name
  remote_virtual_network_id = azurerm_virtual_network.vnet_main.id
}

resource "azurerm_subnet" "default_subnet_target" {
  name                 = "default"
  resource_group_name  = azurerm_resource_group.target.name
  virtual_network_name = azurerm_virtual_network.vnet_target.name
  address_prefixes     = ["10.1.0.0/24"]
}

resource "azurerm_subnet" "psql_subnet_target" {
  count                = var.psql_scenario ? 1 : 0
  name                 = "psql"
  resource_group_name  = azurerm_resource_group.target.name
  virtual_network_name = azurerm_virtual_network.vnet_target.name
  address_prefixes     = ["10.1.1.0/24"]

  delegation {
    name = "psql"
    service_delegation {
      name = "Microsoft.DBforPostgreSQL/flexibleServers"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
      ]
    }
  }
}

resource "azurerm_private_dns_zone_virtual_network_link" "dns_target" {
  count                 = var.psql_scenario ? 1 : 0
  name                  = module.naming_target.virtual_network.name_unique
  private_dns_zone_name = azurerm_private_dns_zone.dns[0].name
  virtual_network_id    = azurerm_virtual_network.vnet_target.id
  resource_group_name   = azurerm_resource_group.target.name

  depends_on = [
    azurerm_subnet.psql_subnet_main,
    azurerm_subnet.psql_subnet_target
  ]
}
