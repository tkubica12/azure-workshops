resource "azurerm_container_group" "httpbin" {
  name                = "httpbin"
  location            = azurerm_resource_group.aks.location
  resource_group_name = azurerm_resource_group.aks.name
  ip_address_type     = "Private"
  subnet_ids          = [azurerm_subnet.aci.id]
  os_type             = "Linux"

  container {
    name   = "httpbin"
    image  = "kong/httpbin"
    cpu    = "0.5"
    memory = "1"

    ports {
      port     = 80
      protocol = "TCP"
    }
  }
}
