resource "azurerm_log_analytics_workspace" "main" {
  name                = random_string.main.result
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_application_insights" "main" {
  name                = random_string.main.result
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  workspace_id        = azurerm_log_analytics_workspace.main.id
  application_type    = "web"
}

resource "azurerm_application_insights_standard_web_test" "testweb_frontdoor" {
  name                    = "web-via-frontdoor"
  location                = azurerm_resource_group.main.location
  resource_group_name     = azurerm_resource_group.main.name
  application_insights_id = azurerm_application_insights.main.id
  retry_enabled           = true
  enabled                 = true
  geo_locations = [
    "emea-nl-ams-azr",
    "emea-gb-db3-azr",
    "emea-ch-zrh-edge",
    "emea-fr-pra-edge",
    "emea-se-sto-edge",
    "emea-ru-msa-edge"
  ]

  request {
    url = "https://${azurerm_cdn_frontdoor_endpoint.main.host_name}/health"
    header {
      name  = "Host"
      value = "web.${element(split("/", var.dns_zone_id), 8)}"
    }
  }
}

resource "azurerm_application_insights_standard_web_test" "testweb_appgw" {
  name                    = "web-via-appgw"
  location                = azurerm_resource_group.main.location
  resource_group_name     = azurerm_resource_group.main.name
  application_insights_id = azurerm_application_insights.main.id
  retry_enabled           = true
  enabled                 = true
  geo_locations = [
    "emea-nl-ams-azr",
    "emea-gb-db3-azr",
    "emea-ch-zrh-edge",
    "emea-fr-pra-edge",
    "emea-se-sto-edge",
    "emea-ru-msa-edge"
  ]

  request {
    url = "https://${azurerm_public_ip.appgw[0].fqdn}/health"
    header {
      name  = "Host"
      value = "web.${element(split("/", var.dns_zone_id), 8)}"
    }
  }
}

resource "azurerm_application_insights_standard_web_test" "testweb" {
  name                    = "web"
  location                = azurerm_resource_group.main.location
  resource_group_name     = azurerm_resource_group.main.name
  application_insights_id = azurerm_application_insights.main.id
  retry_enabled           = true
  enabled                 = true
  geo_locations = [
    "emea-nl-ams-azr",
    "emea-gb-db3-azr",
    "emea-ch-zrh-edge",
    "emea-fr-pra-edge",
    "emea-se-sto-edge",
    "emea-ru-msa-edge"
  ]

  request {
    url = "https://web.${element(split("/", var.dns_zone_id), 8)}/health"
  }
}
