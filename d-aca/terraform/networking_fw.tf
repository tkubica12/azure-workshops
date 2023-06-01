// Azure Firewall
resource "azurerm_public_ip" "fw" {
  name                = "fw-ip"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_public_ip" "fw_management" {
  name                = "fw-management-ip"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_firewall" "main" {
  name                = "aca-fw"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku_name            = "AZFW_VNet"
  sku_tier            = "Basic"
  firewall_policy_id  = azurerm_firewall_policy.main.id

  ip_configuration {
    name                 = "configuration"
    subnet_id            = azurerm_subnet.fw.id
    public_ip_address_id = azurerm_public_ip.fw.id
  }

  management_ip_configuration {
    name                 = "configuration_management"
    subnet_id            = azurerm_subnet.fw_management.id
    public_ip_address_id = azurerm_public_ip.fw_management.id
  }
}

// Policy and rules
resource "azurerm_firewall_policy" "main" {
  name                = "fw-policy"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Basic"
}

resource "azurerm_firewall_policy_rule_collection_group" "main" {
  name               = "fw-policy-rule-collection-group"
  firewall_policy_id = azurerm_firewall_policy.main.id
  priority           = 500

  application_rule_collection {
    name     = "aca"
    priority = 500
    action   = "Allow"
    rule {
      name = "aca"
      protocols {
        type = "Http"
        port = 80
      }
      protocols {
        type = "Https"
        port = 443
      }
      source_addresses = ["0.0.0.0/0"]
      destination_fqdns = [
        "mcr.microsoft.com",
        "*.data.mcr.microsoft.com",
        "*.ghcr.io"
      ]
    }
  }

  network_rule_collection {
    name     = "private"
    priority = 400
    action   = "Allow"
    rule {
      name                  = "private"
      protocols             = ["TCP", "UDP"]
      source_addresses      = ["10.0.0.0/16"]
      destination_addresses = ["10.0.0.0/16"]
      destination_ports     = ["80", "443"]
    }
  }
}
