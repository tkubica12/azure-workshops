resource "azurerm_public_ip" "lb" {
  name                = "lb-ip"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  allocation_method   = "Static"
  sku                 = "Standard"
  zones               = ["1", "2", "3"]
}

resource "azurerm_lb" "main" {
  name                = "lb"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "Standard"

  frontend_ip_configuration {
    name                 = "publicip"
    public_ip_address_id = azurerm_public_ip.lb.id
  }
}

resource "azurerm_lb_backend_address_pool" "main" {
  loadbalancer_id = azurerm_lb.main.id
  name            = "backend"
}

resource "azurerm_lb_probe" "main" {
  loadbalancer_id     = azurerm_lb.main.id
  name                = "web"
  port                = 80
  protocol            = "Http"
  interval_in_seconds = 5
  request_path        = "/"
}

resource "azurerm_lb_rule" "main" {
  loadbalancer_id                = azurerm_lb.main.id
  name                           = "webrule"
  protocol                       = "Tcp"
  frontend_port                  = 80
  backend_port                   = 80
  frontend_ip_configuration_name = azurerm_lb.main.frontend_ip_configuration.0.name
  backend_address_pool_ids = [ azurerm_lb_backend_address_pool.main.id ]
}

# resource "azurerm_lb_outbound_rule" "main" {
#   name                    = "OutboundRule"
#   loadbalancer_id         = azurerm_lb.main.id
#   protocol                = "Tcp"
#   backend_address_pool_id = azurerm_lb_backend_address_pool.main.id

#   frontend_ip_configuration {
#     name = azurerm_lb.main.frontend_ip_configuration.0.name
#   }
# }

resource "azurerm_network_interface_backend_address_pool_association" "vm1" {
  network_interface_id    = azurerm_network_interface.vm1.id
  ip_configuration_name   = azurerm_network_interface.vm1.ip_configuration.0.name
  backend_address_pool_id = azurerm_lb_backend_address_pool.main.id
}

resource "azurerm_network_interface_backend_address_pool_association" "vm2" {
  network_interface_id    = azurerm_network_interface.vm2.id
  ip_configuration_name   = azurerm_network_interface.vm2.ip_configuration.0.name
  backend_address_pool_id = azurerm_lb_backend_address_pool.main.id
}
