resource "azurerm_virtual_network" "hub" {
  name                = "${var.name}-hub"
  resource_group_name = var.rg_name
  location            = var.location
  address_space       = [cidrsubnet(var.ip_range, 8, 0)]
}

resource "azurerm_subnet" "hub_fw" {
  name                 = "AzureFirewallSubnet"
  resource_group_name  = var.rg_name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = [cidrsubnet(azurerm_virtual_network.hub.address_space[0], 2, 0)]
}

resource "azurerm_virtual_network" "spoke1" {
  name                = "${var.name}-spoke1"
  resource_group_name = var.rg_name
  location            = var.location
  address_space       = [cidrsubnet(var.ip_range, 8, 1)]
}

resource "azurerm_subnet" "spoke1_vm" {
  name                 = "default"
  resource_group_name  = var.rg_name
  virtual_network_name = azurerm_virtual_network.spoke1.name
  address_prefixes     = [cidrsubnet(azurerm_virtual_network.spoke1.address_space[0], 2, 0)]
}

resource "azurerm_route_table" "spoke1" {
  name                = "${var.name}-spoke1"
  resource_group_name = var.rg_name
  location            = var.location

  route {
    name                   = "all_via_fw"
    address_prefix         = "0.0.0.0/0"
    next_hop_type          = "VirtualAppliance"
    next_hop_in_ip_address = azurerm_firewall.main.ip_configuration[0].private_ip_address
  }
}

resource "azurerm_subnet_route_table_association" "spoke1_vm" {
  subnet_id      = azurerm_subnet.spoke1_vm.id
  route_table_id = azurerm_route_table.spoke1.id
}
