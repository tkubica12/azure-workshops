
// Origin group - API Management
resource "azurerm_cdn_frontdoor_origin_group" "apim" {
  name                     = "apim"
  cdn_frontdoor_profile_id = azurerm_cdn_frontdoor_profile.main.id

  load_balancing {}
}

// Origin - API Management
resource "azurerm_cdn_frontdoor_origin" "apim" {
  name                           = "apim"
  cdn_frontdoor_origin_group_id  = azurerm_cdn_frontdoor_origin_group.apim.id
  certificate_name_check_enabled = false
  host_name                      = replace(azurerm_api_management.main.gateway_url, "https://", "")
  origin_host_header             = replace(azurerm_api_management.main.gateway_url, "https://", "")
  http_port                      = 80
  https_port                     = 443
  priority                       = 1
  weight                         = 1
  enabled                        = true
}

// Route - API Management
resource "azurerm_cdn_frontdoor_route" "apim_route" {
  name                          = "route-apim"
  cdn_frontdoor_endpoint_id     = azurerm_cdn_frontdoor_endpoint.main.id
  cdn_frontdoor_origin_group_id = azurerm_cdn_frontdoor_origin_group.apim.id
  cdn_frontdoor_origin_ids      = [azurerm_cdn_frontdoor_origin.apim.id]
  forwarding_protocol           = "MatchRequest"
  https_redirect_enabled        = true
  patterns_to_match             = ["/api/*"]
  supported_protocols           = ["Http", "Https"]
  enabled                       = true
}
