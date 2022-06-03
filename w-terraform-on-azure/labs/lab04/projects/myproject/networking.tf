// Virtual Network
resource "azurerm_virtual_network" "demo" {
  name                = "myvnet"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  address_space       = ["10.0.0.0/16"]
}

// Subnets
resource "azurerm_subnet" "vm" {
  name                 = "vm-subnet"
  resource_group_name  = azurerm_resource_group.demo.name
  virtual_network_name = azurerm_virtual_network.demo.name
  address_prefixes     = ["10.0.0.0/24"]
}

resource "azurerm_subnet" "db" {
  name                 = "db-subnet"
  resource_group_name  = azurerm_resource_group.demo.name
  virtual_network_name = azurerm_virtual_network.demo.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_subnet" "webapp" {
  name                 = "webapp-subnet"
  resource_group_name  = azurerm_resource_group.demo.name
  virtual_network_name = azurerm_virtual_network.demo.name
  address_prefixes     = ["10.0.2.0/24"]
}

// Private DNS zone for Azure SQL Private Endpoints
resource "azapi_resource" "privatednssql" {
  type      = "Microsoft.Network/privateDnsZones@2018-09-01"
  name      = "privatelink.database.windows.net"
  parent_id = azurerm_resource_group.demo.id
  location  = "global"
}

// Link Private DNS to VNET
resource "azurerm_private_dns_zone_virtual_network_link" "privatednssql" {
  name                  = "privatednssqllink"
  resource_group_name   = azurerm_resource_group.demo.name
  private_dns_zone_name = azapi_resource.privatednssql.name
  virtual_network_id    = azurerm_virtual_network.demo.id
}