// User managed identity
resource "azurerm_user_assigned_identity" "identity1" {
  name                = "identity1"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
}

// Federation with my AKS
resource "azapi_resource" "identity1" {
  type      = "Microsoft.ManagedIdentity/userAssignedIdentities/federatedIdentityCredentials@2022-01-31-preview"
  name      = "aks-federated-identity"
  parent_id = azurerm_user_assigned_identity.identity1.id
  body = jsonencode({
    properties = {
      audiences = [
        "api://AzureADTokenExchange"
      ]
      issuer  = jsondecode(azapi_resource.aks.output).properties.oidcIssuerProfile.issuerURL
      subject = "system:serviceaccount:default:identity1"
    }
  })
}

// Kubernetes account mapped to user managed identity
resource "kubernetes_service_account" "identity1" {
  metadata {
    name      = "identity1"
    namespace = "default"

    annotations = {
      "azure.workload.identity/client-id" = azurerm_user_assigned_identity.identity1.client_id
    }

    labels = {
      "azure.workload.identity/use" = "true"
    }
  }
}

