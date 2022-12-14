resource "azapi_resource" "aks" {
  type                      = "Microsoft.ContainerService/managedClusters@2022-09-02-preview"
  name                      = "d-managed-prometheus"
  location                  = azurerm_resource_group.main.location
  parent_id                 = azurerm_resource_group.main.id
  schema_validation_enabled = false

  identity {
    type         = "SystemAssigned"
    identity_ids = []
  }

  body = jsonencode({
    properties = {
      addonProfiles = {}
      agentPoolProfiles = [
        {
          count               = 1
          name                = "default"
          orchestratorVersion = "1.23.8"
          osDiskSizeGB        = 128
          osDiskType          = "Managed"
          osSKU               = "Ubuntu"
          osType              = "Linux"
          type                = "VirtualMachineScaleSets"
          vmSize              = "Standard_B2ms"
          mode                = "System"
        }
      ]
      dnsPrefix               = "d-managed-prometheus"
      enablePodSecurityPolicy = false
      enableRBAC              = true
      kubernetesVersion       = "1.23.8"
      networkProfile = {
        dnsServiceIP     = "10.0.0.10"
        dockerBridgeCidr = "172.17.0.1/16"
        loadBalancerProfile = {
          managedOutboundIPs = {
            count = 1
          }
        }
        loadBalancerSku = "Standard"
        networkPlugin   = "kubenet"
        outboundType    = "loadBalancer"
        podCidrs = [
          "10.244.0.0/16"
        ]
        serviceCidrs = [
          "10.0.0.0/16"
        ]
      }
      nodeResourceGroup = "MC_d-managed-prometheus"
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
      azureMonitorProfile = {
        metrics = {
          enabled = true
          kubeStateMetrics = {
            metricLabelsAllowlist      = ""
            metricAnnotationsAllowList = ""
          }
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
}

