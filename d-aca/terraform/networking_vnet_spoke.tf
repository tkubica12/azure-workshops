resource "azurerm_virtual_network" "spoke" {
  name                = "d-aca-spoke"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  address_space       = ["10.66.1.0/24"]
}

resource "azurerm_subnet" "aca_int" {
  name                 = "aca-int"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.spoke.name
  address_prefixes     = ["10.66.1.0/27"]

  delegation {
    name = "Microsoft.App.environments"

    service_delegation {
      name    = "Microsoft.App/environments"
      actions = ["Microsoft.Network/virtualNetworks/subnets/join/action"]
    }
  }
}

