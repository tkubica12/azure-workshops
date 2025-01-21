resource "azurerm_virtual_network" "main" {
  name                = "${local.base_name}-vnet"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "aks" {
  name                            = "aks-subnet"
  resource_group_name             = azurerm_resource_group.main.name
  virtual_network_name            = azurerm_virtual_network.main.name
  address_prefixes                = ["10.0.1.0/24"]
  default_outbound_access_enabled = false
}

resource "azurerm_subnet" "api_server" {
  name                 = "api-server-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.2.0/24"]

  lifecycle {
    ignore_changes = [delegation]
  }
}

resource "azurerm_subnet" "client" {
  name                 = "client-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.3.0/24"]
}

resource "azurerm_subnet" "azure_bastion" {
  name                 = "AzureBastionSubnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.4.0/24"]
}

resource "azurerm_network_security_group" "aks_nsg" {
  name                = "${local.base_name}-aks-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "Deny-Internet-Outbound"
    priority                   = 100
    direction                  = "Outbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "Internet"
  }
}

resource "azurerm_subnet_network_security_group_association" "aks_nsg_association" {
  subnet_id                 = azurerm_subnet.aks.id
  network_security_group_id = azurerm_network_security_group.aks_nsg.id
}

resource "azurerm_subnet_network_security_group_association" "api_server_nsg_association" {
  subnet_id                 = azurerm_subnet.api_server.id
  network_security_group_id = azurerm_network_security_group.aks_nsg.id
}
