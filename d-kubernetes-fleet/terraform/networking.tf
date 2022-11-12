resource "azurerm_virtual_network" "reg1" {
  name                = "kube-fleet-${local.reg1}"
  location            = local.reg1
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.1.0.0/16"]
}

resource "azurerm_subnet" "reg1" {
  name                 = "default"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.reg1.name
  address_prefixes     = ["10.1.0.0/20"]
}

resource "azurerm_virtual_network" "reg2" {
  name                = "kube-fleet-${local.reg2}"
  location            = local.reg2
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.2.0.0/16"]
}

resource "azurerm_subnet" "reg2" {
  name                 = "default"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.reg2.name
  address_prefixes     = ["10.2.0.0/20"]
}

resource "azurerm_virtual_network_peering" "reg1_reg2" {
  name                         = "reg1_reg2"
  resource_group_name          = azurerm_resource_group.main.name
  virtual_network_name         = azurerm_virtual_network.reg1.name
  remote_virtual_network_id    = azurerm_virtual_network.reg2.id
  allow_virtual_network_access = true
  allow_forwarded_traffic      = true
}

resource "azurerm_virtual_network_peering" "reg2_reg1" {
  name                         = "reg2_reg1"
  resource_group_name          = azurerm_resource_group.main.name
  virtual_network_name         = azurerm_virtual_network.reg2.name
  remote_virtual_network_id    = azurerm_virtual_network.reg1.id
  allow_virtual_network_access = true
  allow_forwarded_traffic      = true
}
