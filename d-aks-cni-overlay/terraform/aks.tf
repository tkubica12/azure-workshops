resource "azapi_resource" "aks" {
  type      = "Microsoft.ContainerService/managedClusters@2022-07-02-preview"
  name      = "d-aks-cni-overlay"
  location  = azurerm_resource_group.aks.location
  parent_id = azurerm_resource_group.aks.id
  identity {
    type         = "SystemAssigned"
    identity_ids = []
  }
  body = jsonencode({
    properties = {
      addonProfiles = {}
      agentPoolProfiles = [
        {
          count               = 2
          name                = "default"
          orchestratorVersion = "1.23.8"
          osDiskSizeGB        = 128
          osDiskType          = "Managed"
          osSKU               = "Ubuntu"
          osType              = "Linux"
          type                = "VirtualMachineScaleSets"
          vmSize              = "Standard_B2ms"
          mode                = "System"
          vnetSubnetID        = azurerm_subnet.aks.id
        }
      ]
      dnsPrefix               = "d-aks-federated-identity"
      enablePodSecurityPolicy = false
      enableRBAC              = true
      kubernetesVersion       = "1.23.8"
      networkProfile = {
        dnsServiceIP     = "10.245.0.10"
        dockerBridgeCidr = "172.17.0.1/16"
        loadBalancerSku   = "Standard"
        networkPlugin     = "azure"
        networkPluginMode = "overlay"
        outboundType      = "UserDefinedRouting"
        podCidrs = [
          "10.244.0.0/16"
        ]
        serviceCidrs = [
          "10.245.0.0/16"
        ]
      }
      nodeResourceGroup = "MC_d-aks-cni-overlay"
      storageProfile = {
        blobCSIDriver = {
          enabled = false
        }
        diskCSIDriver = {
          enabled = true
          version = "v1"
        }
        fileCSIDriver = {
          enabled = true
        }
        snapshotController = {
          enabled = true
        }
      }
    }
    sku = {
      name = "Basic"
      tier = "Free"
    }
  })

  response_export_values = [
    "*"
  ]

  depends_on = [
    azurerm_firewall.main
  ]
}
