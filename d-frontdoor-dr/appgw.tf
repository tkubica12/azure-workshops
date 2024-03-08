resource "azurerm_virtual_network" "appgw" {
  count               = var.deploy_appgw ? 1 : 0
  name                = "vnet-appgw"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.appgw_location
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_network_security_group" "appgw" {
  count               = var.deploy_appgw ? 1 : 0
  name                = "nsg-appgw"
  location            = var.appgw_location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "web-http"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "web-https"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_subnet" "appgw" {
  count                = var.deploy_appgw ? 1 : 0
  name                 = "appgw"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.appgw[0].name
  address_prefixes     = ["10.0.0.0/24"]
}

resource "azurerm_subnet_network_security_group_association" "appgw" {
  count                     = var.deploy_appgw ? 1 : 0
  subnet_id                 = azurerm_subnet.appgw[0].id
  network_security_group_id = azurerm_network_security_group.appgw[0].id
}

resource "azurerm_public_ip" "appgw" {
  count               = var.deploy_appgw ? 1 : 0
  name                = "pip-appgw"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.appgw_location
  allocation_method   = "Static"
  sku                 = "Standard"
  domain_name_label   = "webdemo5118"
}

resource "azurerm_application_gateway" "appgw" {
  count               = var.deploy_appgw ? 1 : 0
  name                = "appgw"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.appgw_location

  sku {
    name     = "Standard_v2"
    tier     = "Standard_v2"
    capacity = 2
  }

  gateway_ip_configuration {
    name      = "my-gateway-ip-configuration"
    subnet_id = azurerm_subnet.appgw[0].id
  }

  frontend_port {
    name = "https"
    port = 443
  }

  frontend_ip_configuration {
    name                 = "pip"
    public_ip_address_id = azurerm_public_ip.appgw[0].id
  }

  backend_address_pool {
    name = "web"
    fqdns = [
      azurerm_container_app.webtester.ingress[0].fqdn
    ]
  }

  backend_http_settings {
    name                  = "web"
    cookie_based_affinity = "Disabled"
    path                  = "/"
    port                  = 443
    protocol              = "Https"
    request_timeout       = 60
    host_name             = azurerm_container_app.webtester.ingress[0].fqdn
  }

  http_listener {
    name                           = "listener"
    frontend_ip_configuration_name = "pip"
    frontend_port_name             = "https"
    protocol                       = "Https"
    ssl_certificate_name           = "webdemo"
  }

  request_routing_rule {
    name                       = "rule"
    priority                   = 10
    rule_type                  = "Basic"
    http_listener_name         = "listener"
    backend_address_pool_name  = "web"
    backend_http_settings_name = "web"
  }

  ssl_certificate {
    name = "webdemo"
    data = filebase64("webdemo.pfx")
  }
}
