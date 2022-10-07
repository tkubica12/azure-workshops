resource "azapi_resource" "aks" {
  type      = "Microsoft.ContainerService/managedClusters@2022-07-02-preview"
  name      = "d-aks-federated-identity"
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
      dnsPrefix               = "d-aks-federated-identity"
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
      nodeResourceGroup = "MC_d-aks-federated-identity"
      oidcIssuerProfile = { # Here we enable OpenID Connect
        enabled = true
      }
      securityProfile = {
        workloadIdentity = {
          enabled = true # Here we enable workload identity ("helpers" so platform will provide token exchange and enbale injection of metadata proxy service sidecar)
        }
      }
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
    "properties.oidcIssuerProfile.issuerURL",
    "*"
  ]
}

data "azapi_resource_action" "aks_credentials" {
  type                   = "Microsoft.ContainerService/managedClusters@2022-07-02-preview"
  resource_id            = azapi_resource.aks.id
  action                 = "listClusterAdminCredential"
  response_export_values = ["*"]
}

locals {
  kubeconfig = base64decode(jsondecode(data.azapi_resource_action.aks_credentials.output).kubeconfigs[0].value)
  cluster_ca_certificate = base64decode(yamldecode(local.kubeconfig).clusters[0].cluster.certificate-authority-data)
  client_certificate = base64decode(yamldecode(local.kubeconfig).users[0].user.client-certificate-data)
  client_key = base64decode(yamldecode(local.kubeconfig).users[0].user.client-key-data)
  host = yamldecode(local.kubeconfig).clusters[0].cluster.server
}
