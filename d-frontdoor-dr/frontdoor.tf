resource "azurerm_cdn_frontdoor_profile" "main" {
  name                = "frontdoor"
  resource_group_name = azurerm_resource_group.main.name
  sku_name            = "Standard_AzureFrontDoor"
}

resource "azurerm_cdn_frontdoor_origin_group" "main" {
  name                                                      = "web"
  cdn_frontdoor_profile_id                                  = azurerm_cdn_frontdoor_profile.main.id
  session_affinity_enabled                                  = true
  restore_traffic_time_to_healed_or_new_endpoint_in_minutes = 10

  health_probe {
    interval_in_seconds = 240
    path                = "/health"
    protocol            = "Https"
    request_type        = "HEAD"
  }

  load_balancing {
    additional_latency_in_milliseconds = 0
    sample_size                        = 16
    successful_samples_required        = 3
  }
}

resource "azurerm_cdn_frontdoor_origin" "main" {
  name                           = "web"
  cdn_frontdoor_origin_group_id  = azurerm_cdn_frontdoor_origin_group.main.id
  enabled                        = true
  certificate_name_check_enabled = false
  host_name                      = azurerm_container_app.httpbin.ingress[0].fqdn
  http_port                      = 80
  https_port                     = 443
  origin_host_header             = azurerm_container_app.httpbin.ingress[0].fqdn
  priority                       = 1
  weight                         = 1
}

resource "azurerm_cdn_frontdoor_endpoint" "main" {
  name                     = "main"
  cdn_frontdoor_profile_id = azurerm_cdn_frontdoor_profile.main.id
}

resource "azurerm_cdn_frontdoor_route" "main" {
  name                          = "main-route"
  cdn_frontdoor_endpoint_id     = azurerm_cdn_frontdoor_endpoint.main.id
  cdn_frontdoor_origin_group_id = azurerm_cdn_frontdoor_origin_group.main.id
  cdn_frontdoor_origin_ids      = [azurerm_cdn_frontdoor_origin.main.id]
  #   cdn_frontdoor_rule_set_ids    = [azurerm_cdn_frontdoor_rule_set.example.id]
  enabled                         = true
  forwarding_protocol             = "HttpsOnly"
  https_redirect_enabled          = true
  patterns_to_match               = ["/*"]
  supported_protocols             = ["Http", "Https"]
  cdn_frontdoor_custom_domain_ids = [azurerm_cdn_frontdoor_custom_domain.main.id]
  link_to_default_domain          = true
}

resource "azurerm_cdn_frontdoor_custom_domain" "main" {
  name                     = "web-demo-tkubica-biz"
  cdn_frontdoor_profile_id = azurerm_cdn_frontdoor_profile.main.id
  dns_zone_id              = var.dns_zone_id
  host_name                = "web.demo.tkubica.biz"

  tls {
    certificate_type    = "ManagedCertificate"
    minimum_tls_version = "TLS12"
  }
}

resource "azurerm_dns_txt_record" "validation" {
  name                = "_dnsauth.web"
  zone_name           = element(split("/", var.dns_zone_id), 8)
  resource_group_name = element(split("/", var.dns_zone_id), 4)
  ttl                 = 300

  record {
    value = azurerm_cdn_frontdoor_custom_domain.main.validation_token
  }
}

# resource "azurerm_cdn_frontdoor_custom_domain_association" "main" {
#   cdn_frontdoor_custom_domain_id = azurerm_cdn_frontdoor_custom_domain.main.id
#   cdn_frontdoor_route_ids        = [azurerm_cdn_frontdoor_route.main.id]
# }