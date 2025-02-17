resource "azurerm_api_management_api" "openai" {
  name                = "openai-api"
  resource_group_name = azurerm_resource_group.main.name
  api_management_name = azurerm_api_management.main.name
  revision            = "1"
  display_name        = "OpenAI API"
  path                = "openai"
  protocols           = ["https"]

  import {
    content_format = "openapi+json"
    content_value  = file("${path.module}/openai_api_spec.json")
  }
}

resource "azapi_resource" "openai_api_diagnostics" {
  type      = "Microsoft.ApiManagement/service/apis/diagnostics@2024-06-01-preview"
  name      = "applicationinsights"
  parent_id = azurerm_api_management_api.openai.id
  body      = {
    properties = {
      alwaysLog               = "allErrors"
      loggerId                = azurerm_api_management_logger.main.id
      metrics                 = true
      httpCorrelationProtocol = "W3C"
      sampling = {
        percentage   = 100
        samplingType = "fixed"
      }
      verbosity = "information"
      frontend = {
        request = {
          body    = { bytes = 32 }
          headers = [ "content-type", "accept", "origin" ]
        }
        response = {
          body    = { bytes = 32 }
          headers = [ "content-type", "content-length", "origin" ]
        }
      }
      backend = {
        request = {
          body    = { bytes = 32 }
          headers = [ "content-type", "accept", "origin" ]
        }
        response = {
          body    = { bytes = 32 }
          headers = [ "content-type", "content-length", "origin" ]
        }
      }
    }
  }
}
