// Origin group - frontend
resource "azurerm_cdn_frontdoor_origin_group" "bookapp_frontend" {
  name                     = "bookapp-frontend"
  cdn_frontdoor_profile_id = azurerm_cdn_frontdoor_profile.main.id

  load_balancing {}
}

// Origin - frontend
resource "azurerm_cdn_frontdoor_origin" "bookapp_frontend" {
  name                           = "bookapp-frontend"
  cdn_frontdoor_origin_group_id  = azurerm_cdn_frontdoor_origin_group.bookapp_frontend.id
  certificate_name_check_enabled = false
  host_name                      = azurerm_container_app.bookapp_frontend.ingress[0].fqdn
  origin_host_header             = azurerm_container_app.bookapp_frontend.ingress[0].fqdn
  http_port                      = 80
  https_port                     = 443
  priority                       = 1
  weight                         = 1
  enabled                        = true
}

// Route - frontend
resource "azurerm_cdn_frontdoor_route" "main" {
  name                          = "route-bookapp-frontend"
  cdn_frontdoor_endpoint_id     = azurerm_cdn_frontdoor_endpoint.main.id
  cdn_frontdoor_origin_group_id = azurerm_cdn_frontdoor_origin_group.bookapp_frontend.id
  cdn_frontdoor_origin_ids      = [azurerm_cdn_frontdoor_origin.bookapp_frontend.id]
  forwarding_protocol           = "MatchRequest"
  https_redirect_enabled        = true
  patterns_to_match             = ["/*"]
  supported_protocols           = ["Http", "Https"]
  enabled                       = true
}
