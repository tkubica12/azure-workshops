
resource "azurerm_dns_cname_record" "example" {
  name                = "web"
  zone_name           = element(split("/", var.dns_zone_id), 8)
  resource_group_name = element(split("/", var.dns_zone_id), 4)
  ttl                 = 60  // just for demo, use 300 for production
  record              = var.traffic_via_fd ? azurerm_cdn_frontdoor_endpoint.main.host_name : azurerm_public_ip.appgw[0].fqdn
}
