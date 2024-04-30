resource "azurerm_lb" "main" {
  name                = module.naming.lb.name
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = "Standard"

  frontend_ip_configuration {
    name                          = "ilb"
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = var.subnet_id
  }
}

resource "azurerm_lb_rule" "main" {
  loadbalancer_id                = azurerm_lb.main.id
  name                           = "web"
  protocol                       = "Tcp"
  frontend_port                  = 80
  backend_port                   = 80
  probe_id                       = azurerm_lb_probe.main.id
  frontend_ip_configuration_name = "ilb"
  backend_address_pool_ids       = [azurerm_lb_backend_address_pool.main.id]
}

resource "azurerm_lb_backend_address_pool" "main" {
  loadbalancer_id = azurerm_lb.main.id
  name            = "backend"
}

resource "azurerm_lb_probe" "main" {
  loadbalancer_id = azurerm_lb.main.id
  name            = "web-probe"
  port            = 80
  protocol        = "Http"
  request_path    = "/"
}
