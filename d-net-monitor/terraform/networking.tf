// Virtual Networks
resource "azurerm_virtual_network" "location1" {
  name                = "d-net-monitor-${var.location1}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_virtual_network" "location2" {
  name                = "d-net-monitor-${var.location2}"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location2
  address_space       = ["10.1.0.0/16"]
}

// Virtual Network Peering
resource "azurerm_virtual_network_peering" "location1" {
  name                         = "peering-${var.location1}-${var.location2}"
  resource_group_name          = azurerm_resource_group.main.name
  virtual_network_name         = azurerm_virtual_network.location1.name
  remote_virtual_network_id    = azurerm_virtual_network.location2.id
  allow_virtual_network_access = true
  allow_forwarded_traffic      = true
  allow_gateway_transit        = false
}

resource "azurerm_virtual_network_peering" "location2" {
  name                         = "peering-${var.location2}-${var.location1}"
  resource_group_name          = azurerm_resource_group.main.name
  virtual_network_name         = azurerm_virtual_network.location2.name
  remote_virtual_network_id    = azurerm_virtual_network.location1.id
  allow_virtual_network_access = true
  allow_forwarded_traffic      = true
  allow_gateway_transit        = false
}

// Subnets
resource "azurerm_subnet" "location1" {
  name                 = "default"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.location1.name
  address_prefixes     = ["10.0.0.0/24"]
}

resource "azurerm_subnet" "location2" {
  name                 = "default"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.location2.name
  address_prefixes     = ["10.1.0.0/24"]
}

// Network Security Groups
resource "azurerm_network_security_group" "location1" {
  name                = "allow-all-${var.location1}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
}

resource "azurerm_network_security_group" "location2" {
  name                = "allow-all-${var.location2}"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location2
}

// Network Security Rules
resource "azurerm_network_security_rule" "location1" {
  name                        = "allow-all"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "*"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.main.name
  network_security_group_name = azurerm_network_security_group.location1.name
}

resource "azurerm_network_security_rule" "location2" {
  name                        = "allow-all"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "*"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.main.name
  network_security_group_name = azurerm_network_security_group.location2.name
}

// NSG association
resource "azurerm_subnet_network_security_group_association" "location1" {
  subnet_id                 = azurerm_subnet.location1.id
  network_security_group_id = azurerm_network_security_group.location1.id
}

resource "azurerm_subnet_network_security_group_association" "location2" {
  subnet_id                 = azurerm_subnet.location2.id
  network_security_group_id = azurerm_network_security_group.location2.id
}

// Enable flow logs
resource "azurerm_network_watcher_flow_log" "location1" {
  network_watcher_name = local.network_watcher_name_location1
  resource_group_name  = local.network_watcher_rg_location1
  name                 = "flow-${azurerm_network_security_group.location1.name}"

  network_security_group_id = azurerm_network_security_group.location1.id
  storage_account_id        = azurerm_storage_account.location1.id
  enabled                   = true

  retention_policy {
    enabled = true
    days    = 7
  }

  traffic_analytics {
    enabled               = true
    workspace_id          = azurerm_log_analytics_workspace.main.workspace_id
    workspace_region      = azurerm_log_analytics_workspace.main.location
    workspace_resource_id = azurerm_log_analytics_workspace.main.id
    interval_in_minutes   = 10
  }
}

resource "azurerm_network_watcher_flow_log" "location2" {
  network_watcher_name = local.network_watcher_name_location2
  resource_group_name  = local.network_watcher_rg_location2
  name                 = "flow-${azurerm_network_security_group.location2.name}"

  network_security_group_id = azurerm_network_security_group.location2.id
  storage_account_id        = azurerm_storage_account.location2.id
  enabled                   = true

  retention_policy {
    enabled = true
    days    = 7
  }

  traffic_analytics {
    enabled               = true
    workspace_id          = azurerm_log_analytics_workspace.main.workspace_id
    workspace_region      = azurerm_log_analytics_workspace.main.location
    workspace_resource_id = azurerm_log_analytics_workspace.main.id
    interval_in_minutes   = 10
  }
}