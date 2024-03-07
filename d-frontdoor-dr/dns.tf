
resource "azurerm_dns_cname_record" "example" {
  name                = "web"
  zone_name           = element(split("/", var.dns_zone_id), 8)
  resource_group_name = element(split("/", var.dns_zone_id), 4)
  ttl                 = 300
  record              = var.traffic_via_fd ? azurerm_cdn_frontdoor_endpoint.main.host_name : "string2"
}
