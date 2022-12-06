// User managed identity
resource "azurerm_user_assigned_identity" "storage_access" {
  name                = "storage_access"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
}

resource "azurerm_user_assigned_identity" "kv_access" {
  name                = "kv_access"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
}

// Federation with my AKS
resource "azapi_resource" "storage_access" {
  type      = "Microsoft.ManagedIdentity/userAssignedIdentities/federatedIdentityCredentials@2022-01-31-preview"
  name      = "storage_access"
  parent_id = azurerm_user_assigned_identity.storage_access.id
  body = jsonencode({
    properties = {
      audiences = [
        "api://AzureADTokenExchange"
      ]
      issuer  = azurerm_kubernetes_cluster.main.oidc_issuer_url
      subject = "system:serviceaccount:default:storageaccess"
    }
  })
}

resource "azapi_resource" "kv_access" {
  type      = "Microsoft.ManagedIdentity/userAssignedIdentities/federatedIdentityCredentials@2022-01-31-preview"
  name      = "kv_access"
  parent_id = azurerm_user_assigned_identity.kv_access.id
  body = jsonencode({
    properties = {
      audiences = [
        "api://AzureADTokenExchange"
      ]
      issuer  = azurerm_kubernetes_cluster.main.oidc_issuer_url
      subject = "system:serviceaccount:default:kvaccess"
    }
  })
}