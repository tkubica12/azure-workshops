resource "azapi_resource" "embeddings_backend" {
  name                      = "embeddings-backend"
  type                      = "Microsoft.ApiManagement/service/backends@2024-06-01-preview"
  parent_id                 = azurerm_api_management.main.id
  location                  = azurerm_resource_group.main.location
  schema_validation_enabled = false

  body = {
    properties = {
      title    = null
      url      = "${azapi_resource.ai_service_p1.output.properties.endpoints["OpenAI Language Model Instance API"]}openai/deployments/${azurerm_cognitive_deployment.embeddings.name}/embeddings"
      protocol = "http"
      credentials = {
        query  = {}
        header = {}
        # managedIdentity = {
        #   resource = "https://cognitiveservices.azure.com/"
        #   clientId = "0fa9aabe-4bf2-4eb6-b7c2-cc253b305b69"
        # }
      }
      tls = {
        validateCertificateChain = true
        validateCertificateName  = true
      }
    }
  }
}
