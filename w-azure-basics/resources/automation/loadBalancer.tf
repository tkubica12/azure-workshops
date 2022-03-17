resource "azurerm_public_ip" "demo" {
  name                = "${var.prefix}-ip"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  allocation_method   = "Static"
  sku                 = "Standard"
  sku_tier            = "Regional"
}

resource "azurerm_lb" "demo" {
  name                = "${var.prefix}-lb"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  sku                 = "Standard"
  sku_tier            = "Regional"

  frontend_ip_configuration {
    name                 = "frontend"
    public_ip_address_id = azurerm_public_ip.demo.id
  }
}

resource "azurerm_lb_backend_address_pool" "demo" {
  loadbalancer_id = azurerm_lb.demo.id
  name            = "backend"
}

resource "azurerm_lb_probe" "demo" {
  resource_group_name = azurerm_resource_group.demo.name
  loadbalancer_id     = azurerm_lb.demo.id
  name                = "web-probe"
  protocol            = "Http"
  port                = 80
  request_path        = "/"
}

resource "azurerm_lb_rule" "demo" {
  resource_group_name            = azurerm_resource_group.demo.name
  loadbalancer_id                = azurerm_lb.demo.id
  name                           = "webrule"
  protocol                       = "Tcp"
  frontend_port                  = 80
  backend_port                   = 80
  frontend_ip_configuration_name = "frontend"
  probe_id                       = azurerm_lb_probe.demo.id
  disable_outbound_snat          = false
  backend_address_pool_ids       = [azurerm_lb_backend_address_pool.demo.id]
}
