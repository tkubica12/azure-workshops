resource "azurerm_virtual_wan" "vwan" {
  name                = "workshop-vwan"
  resource_group_name = azurerm_resource_group.workshop.name
  location            = azurerm_resource_group.workshop.location
}

resource "azurerm_virtual_hub" "vwan" {
  name                = "workshop-hub"
  resource_group_name = azurerm_resource_group.workshop.name
  location            = azurerm_resource_group.workshop.location
  virtual_wan_id      = azurerm_virtual_wan.vwan.id
  address_prefix      = "10.255.0.0/16"
  sku                 = "Standard"
}

resource "azurerm_virtual_network" "sharedVnet" {
  name                = "shared-vnet"
  location            = azurerm_resource_group.workshop.location
  resource_group_name = azurerm_resource_group.workshop.name
  address_space       = ["10.254.0.0/16"]
}

resource "azurerm_subnet" "sharedVnetSubnet" {
  name                 = "default"
  resource_group_name  = azurerm_resource_group.workshop.name
  virtual_network_name = azurerm_virtual_network.sharedVnet.name
  address_prefixes     = ["10.254.0.0/24"]
}

resource "azurerm_virtual_hub_connection" "sharedVnet" {
  name                      = "sharedVnet"
  virtual_hub_id            = azurerm_virtual_hub.vwan.id
  remote_virtual_network_id = azurerm_virtual_network.sharedVnet.id
}