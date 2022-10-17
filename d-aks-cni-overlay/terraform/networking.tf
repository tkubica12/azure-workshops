// VNET
resource "azurerm_virtual_network" "main" {
  name                = "d-aks-cni-overlay-vnet"
  resource_group_name = azurerm_resource_group.networking.name
  location            = azurerm_resource_group.networking.location
  address_space       = ["10.99.0.0/16"]
}

// Firewall subnet
resource "azurerm_subnet" "firewall" {
  name                 = "AzureFirewallSubnet"
  resource_group_name  = azurerm_resource_group.networking.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.99.0.0/24"]
}

resource "azurerm_subnet" "firewall_management" {
  name                 = "AzureFirewallManagementSubnet"
  resource_group_name  = azurerm_resource_group.networking.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.99.1.0/24"]
}

// AKS subnet
resource "azurerm_subnet" "aks" {
  name                 = "aks"
  resource_group_name  = azurerm_resource_group.networking.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.99.2.0/24"]
}

// ACI subnet
resource "azurerm_subnet" "aci" {
  name                 = "aci"
  resource_group_name  = azurerm_resource_group.networking.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.99.3.0/24"]

  delegation {
    name = "delegation"

    service_delegation {
      name    = "Microsoft.ContainerInstance/containerGroups"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

// UDR
resource "azurerm_route_table" "main" {
  name                = "d-aks-cni-overlay-udr"
  resource_group_name = azurerm_resource_group.networking.name
  location            = azurerm_resource_group.networking.location

  route = [
    {
      name                   = "all_via_fw"
      address_prefix         = "0.0.0.0/0"
      next_hop_in_ip_address = azurerm_firewall.main.ip_configuration[0].private_ip_address
      next_hop_type          = "VirtualAppliance"
    }
  ]
}

resource "azurerm_subnet_route_table_association" "main" {
  route_table_id = azurerm_route_table.main.id
  subnet_id      = azurerm_subnet.aks.id
}

// Firewall policy
resource "azurerm_firewall_policy" "main" {
  name                = "d-aks-cni-overlay-fw-policy"
  resource_group_name = azurerm_resource_group.networking.name
  location            = azurerm_resource_group.networking.location
  sku                 = "Standard"
}

resource "azurerm_firewall_policy_rule_collection_group" "main" {
  name               = "any"
  firewall_policy_id = azurerm_firewall_policy.main.id
  priority           = 200

  network_rule_collection {
    name     = "any"
    priority = 100
    action   = "Allow"
    rule {
      name                  = "any"
      protocols             = ["TCP", "UDP"]
      source_addresses      = ["*"]
      destination_addresses = ["*"]
      destination_ports     = ["*"]
    }
  }
}

// Firewall IP
resource "azurerm_public_ip" "firewall" {
  name                = "d-aks-cni-overlay-fw-ip"
  resource_group_name = azurerm_resource_group.networking.name
  location            = azurerm_resource_group.networking.location
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_public_ip" "firewall_management" {
  name                = "d-aks-cni-overlay-fw-ip-mgmt"
  resource_group_name = azurerm_resource_group.networking.name
  location            = azurerm_resource_group.networking.location
  allocation_method   = "Static"
  sku                 = "Standard"
}

// Firewall basic
resource "azurerm_firewall" "main" {
  name                = "d-aks-cni-overlay-fw"
  location            = azurerm_resource_group.networking.location
  resource_group_name = azurerm_resource_group.networking.name
  firewall_policy_id  = azurerm_firewall_policy.main.id
  sku_name            = "AZFW_VNet"
  sku_tier            = "Standard"

  ip_configuration {
    name                 = "ipconfig"
    subnet_id            = azurerm_subnet.firewall.id
    public_ip_address_id = azurerm_public_ip.firewall.id
  }

  management_ip_configuration {
    name                 = "ipconfig_management"
    subnet_id            = azurerm_subnet.firewall_management.id
    public_ip_address_id = azurerm_public_ip.firewall_management.id
  }
}

