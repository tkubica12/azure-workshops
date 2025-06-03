resource "azapi_resource" "storage_account_main" {
  type      = "Microsoft.Storage/storageAccounts@2024-01-01"
  name      = "st${local.base_name_nodash}"
  parent_id = azurerm_resource_group.main.id
  location  = azurerm_resource_group.main.location

  body = {
    sku = {
      name = "Standard_LRS"
    }
    kind = "StorageV2"
    properties = {
      defaultToOAuthAuthentication = true
      isLocalUserEnabled           = false
      supportsHttpsTrafficOnly     = true
      minimumTlsVersion            = "TLS1_2"
      allowBlobPublicAccess        = false
    }
  }
}
