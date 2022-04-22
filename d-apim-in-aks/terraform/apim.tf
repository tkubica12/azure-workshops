// APIM
resource "azurerm_api_management" "demo" {
  name                 = "apim${random_string.random.result}"
  location             = azurerm_resource_group.demo.location
  resource_group_name  = azurerm_resource_group.demo.name
  publisher_name       = "Tomas Demo"
  publisher_email      = "tomas@demo.demo"
  virtual_network_type = "None"
  sku_name             = "Premium_1"
}

// Self-hosted gateway registration
resource "azurerm_api_management_gateway" "demo" {
  name              = "demogw"
  api_management_id = azurerm_api_management.demo.id
  description       = "Example API Management gateway"

  location_data {
    name     = "example name"
    city     = "example city"
    district = "example district"
    region   = "example region"
  }
}

// API
resource "azurerm_api_management_api" "demo" {
  name                  = "demo-api"
  resource_group_name   = azurerm_resource_group.demo.name
  api_management_name   = azurerm_api_management.demo.name
  revision              = "1"
  display_name          = "Demo API"
  path                  = "demo"
  protocols             = ["http"]
  subscription_required = false
}

resource "azurerm_api_management_api_operation" "demo" {
  operation_id        = "get-mock-demo"
  api_name            = azurerm_api_management_api.demo.name
  api_management_name = azurerm_api_management_api.demo.api_management_name
  resource_group_name = azurerm_api_management_api.demo.resource_group_name
  display_name        = "Get mocked demo items"
  method              = "GET"
  url_template        = "/demo/items"
  description         = "This is demo operation"

  response {
    status_code = 200
    representation {
      content_type = "application/json"
      example {
        name = "default"
        value = jsonencode({"items" = ["demo1", "demo2"]})
      }
    }
  }
}

resource "azurerm_api_management_api_operation_policy" "demo" {
  api_name            = azurerm_api_management_api_operation.demo.api_name
  api_management_name = azurerm_api_management_api_operation.demo.api_management_name
  resource_group_name = azurerm_api_management_api_operation.demo.resource_group_name
  operation_id        = azurerm_api_management_api_operation.demo.operation_id

  xml_content = <<XML
<policies>
  <inbound>
    <mock-response status-code="200" content-type="application/json" />
  </inbound>
</policies>
XML

}

// Map API to gateway
resource "azurerm_api_management_gateway_api" "demo" {
  gateway_id = azurerm_api_management_gateway.demo.id
  api_id     = azurerm_api_management_api.demo.id
}

// Output
output "gateway_id" {
  value = azurerm_api_management_gateway.demo.id
}

output "apim_name" {
  value = azurerm_api_management.demo.name
}