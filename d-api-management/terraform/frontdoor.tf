resource "azurerm_cdn_frontdoor_profile" "main" {
  name                = "afd-${local.base_name}"
  resource_group_name = azurerm_resource_group.main.name
  sku_name            = "Standard_AzureFrontDoor"
}

resource "azurerm_cdn_frontdoor_endpoint" "main" {
  name                     = "fde-${local.base_name}"
  cdn_frontdoor_profile_id = azurerm_cdn_frontdoor_profile.main.id
}
