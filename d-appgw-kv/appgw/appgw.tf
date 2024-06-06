
resource "azurerm_public_ip" "appgw_pip" {
  name                = "appgw-pip"
  resource_group_name = var.resource_group_name
  location            = var.location
  allocation_method   = "Static"
  sku                 = "Standard"
}


resource "azurerm_application_gateway" "main" {
  name                = "appgw"
  resource_group_name = var.resource_group_name
  location            = var.location

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.appgw.id]
  }

  sku {
    name     = "Standard_v2"
    tier     = "Standard_v2"
    capacity = 2
  }

  gateway_ip_configuration {
    name      = "ipconfig"
    subnet_id = var.subnet_id_appgw
  }

  frontend_port {
    name = "https"
    port = 443
  }

  frontend_ip_configuration {
    name      = "front"
    subnet_id = var.privatedns_id
  }

  backend_address_pool {
    name = "pool"
  }

  backend_http_settings {
    name                  = "http"
    cookie_based_affinity = "Disabled"
    path                  = "/"
    port                  = 80
    protocol              = "Http"
    request_timeout       = 60
  }

  http_listener {
    name                           = "listener"
    frontend_ip_configuration_name = "front"
    frontend_port_name             = "https"
    protocol                       = "Https"
    ssl_certificate_name           = "cert"
  }

  request_routing_rule {
    name                       = "myrule"
    priority                   = 10
    rule_type                  = "Basic"
    http_listener_name         = "listener"
    backend_address_pool_name  = "pool"
    backend_http_settings_name = "http"
  }

  ssl_certificate {
    name                = "cert"
    key_vault_secret_id = azurerm_key_vault_certificate.main.secret_id
  }
}
