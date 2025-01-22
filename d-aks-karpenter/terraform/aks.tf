resource "azapi_resource" "aks_cluster" {
  type      = "Microsoft.ContainerService/managedClusters@2024-09-02-preview"
  parent_id = azurerm_resource_group.main.id
  name      = local.base_name
  location  = azurerm_resource_group.main.location

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.main.id]
  }

  body = {
    properties = {
      dnsPrefix = local.base_name
      agentPoolProfiles = [
        {
          name         = "default"
          mode         = "System"
          vmSize       = "Standard_B4ms"
          count        = 1
          vnetSubnetID = azurerm_subnet.aks.id
        }
      ]
      nodeProvisioningProfile = {
        mode = "Auto"
      }
      networkProfile = {
        networkPlugin     = "azure"
        networkPluginMode = "overlay"
        networkDataplane  = "cilium"
        networkPolicy     = "cilium"
        podCidr           = "10.233.0.0/16"
        serviceCidr       = "10.234.0.0/16"
        dnsServiceIP      = "10.234.10.10"
        outboundType      = "loadBalancer"
      }
    }
  }

  response_export_values = ["*"]
}
