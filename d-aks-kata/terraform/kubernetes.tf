resource "azurerm_virtual_network" "main" {
  name                = "d-aks-kata-vnet"
  address_space       = ["10.10.0.0/16"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_subnet" "aks" {
  name                 = "d-aks-kata-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.10.0.0/24"]
}

resource "azapi_resource" "aks" {
  type      = "Microsoft.ContainerService/managedClusters@2022-07-02-preview"
  name      = "d-aks-kata"
  location  = azurerm_resource_group.main.location
  parent_id = azurerm_resource_group.main.id
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
          orchestratorVersion = "1.25.5"
          osDiskSizeGB        = 128
          osDiskType          = "Ephemeral"
          osSKU               = "Mariner"
          osType              = "Linux"
          type                = "VirtualMachineScaleSets"
          vmSize              = "Standard_D16s_v3"
          mode                = "System"
          vnetSubnetID        = azurerm_subnet.aks.id
          workloadRuntime     = "KataMshvVmIsolation"
        }
      ]
      dnsPrefix               = "d-aks-kata"
      enablePodSecurityPolicy = false
      enableRBAC              = true
      kubernetesVersion       = "1.25.5"
      networkProfile = {
        dnsServiceIP      = "10.245.0.10"
        dockerBridgeCidr  = "172.17.0.1/16"
        loadBalancerSku   = "Standard"
        networkPlugin     = "azure"
        networkPluginMode = "overlay"
        outboundType      = "LoadBalancer"
        podCidrs = [
          "10.244.0.0/16"
        ]
        serviceCidrs = [
          "10.245.0.0/16"
        ]
      }
      nodeResourceGroup = "MC_d-aks-kata"
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
}

# resource "azapi_resource" "flux_extension" {
#   type      = "Microsoft.KubernetesConfiguration/extensions@2021-09-01"
#   name      = "flux"
#   parent_id = azapi_resource.aks.id

#   body = jsonencode({
#     properties = {
#       extensionType           = "microsoft.flux"
#       autoUpgradeMinorVersion = true
#     }
#   })
# }

# resource "azapi_resource" "flux_config" {
#   type                      = "Microsoft.KubernetesConfiguration/fluxConfigurations@2022-03-01"
#   name                      = "mydemo"
#   parent_id                 = azapi_resource.aks.id
#   schema_validation_enabled = false

#   depends_on = [
#     azapi_resource.flux_extension
#   ]

#   body = jsonencode({
#     properties = {
#       scope      = "cluster"
#       namespace  = "flux-system"
#       sourceKind = "GitRepository"
#       kustomizations = {
#         myapp = {
#           name                   = "mydemo"
#           path                   = "./d-aks-kata/kubernetes"
#           force                  = true
#           prune                  = true
#           timeoutInSeconds       = 120
#           intervalInSeconds      = 120
#           retryIntervalInSeconds = 120
#         }
#       }
#       gitRepository = {
#         url                   = "https://github.com/tkubica12/azure-workshops"
#         timeoutInSeconds      = 120
#         syncIntervalInSeconds = 120
#         repositoryRef = {
#           branch = "main"
#         }
#       }
#     }
#   })
# }

