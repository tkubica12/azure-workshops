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
      networkProfile = {
        networkPlugin              = "cilium"
        networkPluginMode          = "overlay"
        networkDataplane           = "cilium"
        networkPolicy              = "cilium"
        podCidr                    = "10.233.0.0/16"
        serviceCidr                = "10.234.0.0/16"
        dnsServiceIP               = "10.234.10.10"
        outboundType               = "loadBalancer"
        staticEgressGatewayProfile = { enabled = true }
      }
    }
  }

  response_export_values = ["*"]
}

resource "azapi_resource" "gateway_node_pool" {
  type      = "Microsoft.ContainerService/managedClusters/agentPools@2024-09-02-preview"
  parent_id = azapi_resource.aks_cluster.id
  name      = "gatewaypool"

  body = {
    properties = {
      mode              = "Gateway"
      osType            = "Linux"
      vmSize            = "Standard_B2ms"
      count             = 2
      enableAutoScaling = false
      vnetSubnetID      = azurerm_subnet.segw.id

      gatewayProfile = {
        publicIPPrefixSize = 31
      }
    }
  }
}
