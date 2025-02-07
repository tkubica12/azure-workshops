resource "azurerm_api_management_backend" "p1" {
  name                = "p1-backend"
  resource_group_name = azurerm_resource_group.main.name
  api_management_name = azurerm_api_management.main.name
  protocol            = "http"
  url                 = "${azapi_resource.ai_service_p1.output.properties.endpoints["OpenAI Language Model Instance API"]}/openai/deployments/${azurerm_cognitive_deployment.openai_model_p1.name}"

  tls {
    validate_certificate_chain = true
    validate_certificate_name  = true
  }
}

resource "azurerm_api_management_backend" "p2" {
  name                = "p2-backend"
  resource_group_name = azurerm_resource_group.main.name
  api_management_name = azurerm_api_management.main.name
  protocol            = "http"
  url                 = "${azapi_resource.ai_service_p2.output.properties.endpoints["OpenAI Language Model Instance API"]}/openai/deployments/${azurerm_cognitive_deployment.openai_model_p2.name}"

  tls {
    validate_certificate_chain = true
    validate_certificate_name  = true
  }
}
