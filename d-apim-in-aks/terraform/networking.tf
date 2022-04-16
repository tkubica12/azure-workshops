// VNET
resource "azurerm_virtual_network" "demo" {
  name                = "apim-demo-aks-vnet"
  resource_group_name = azurerm_resource_group.demo.name
  location            = var.location
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "aks" {
  name                 = "aks"
  resource_group_name  = azurerm_resource_group.demo.name
  virtual_network_name = azurerm_virtual_network.demo.name
  address_prefixes     = ["10.0.0.0/24"]
}

resource "azurerm_subnet" "jump" {
  name                 = "jump"
  resource_group_name  = azurerm_resource_group.demo.name
  virtual_network_name = azurerm_virtual_network.demo.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_subnet" "fw" {
  name                 = "AzureFirewallSubnet"
  resource_group_name  = azurerm_resource_group.demo.name
  virtual_network_name = azurerm_virtual_network.demo.name
  address_prefixes     = ["10.0.2.0/24"]
}

// Routing
resource "azurerm_route_table" "demo" {
  name                          = "all-via-fw"
  location                      = azurerm_resource_group.demo.location
  resource_group_name           = azurerm_resource_group.demo.name
  disable_bgp_route_propagation = false

  route {
    name                   = "default"
    address_prefix         = "0.0.0.0/0"
    next_hop_type          = "VirtualAppliance"
    next_hop_in_ip_address = azurerm_firewall.demo.ip_configuration.0.private_ip_address
  }
}

resource "azurerm_subnet_route_table_association" "jump" {
  subnet_id      = azurerm_subnet.jump.id
  route_table_id = azurerm_route_table.demo.id
}

resource "azurerm_subnet_route_table_association" "aks" {
  subnet_id      = azurerm_subnet.aks.id
  route_table_id = azurerm_route_table.demo.id
}

// Firewall policy
resource "azurerm_firewall_policy" "demo" {
  name                = "mypolicy"
  sku                 = "Standard"
  resource_group_name = azurerm_resource_group.demo.name
  location            = var.location
}

// Firewall
resource "azurerm_public_ip" "fw" {
  name                = "fwip"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_firewall" "demo" {
  name                = "fw"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  sku_name            = "AZFW_VNet"
  sku_tier            = "Standard"
  firewall_policy_id  = azurerm_firewall_policy.demo.id

  ip_configuration {
    name                 = "configuration"
    subnet_id            = azurerm_subnet.fw.id
    public_ip_address_id = azurerm_public_ip.fw.id
  }
}
