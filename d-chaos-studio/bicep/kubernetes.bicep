/*
  This module deploys Azure Kubernetes Service
  together with GitOps to spin up application pods
  and Chaos Mesh (dependency for Azure Chaos Studio)
*/

param subnetId string
param location string

resource aksIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2022-01-31-preview' = {
  name: 'aksIdentity'
  location: location
}

resource aksIdentityRbac 'Microsoft.Authorization/roleAssignments@2020-10-01-preview' = {
  name: guid('aksIdentityRbac')
  scope: resourceGroup()
  properties: {
    principalId: aksIdentity.properties.principalId
    roleDefinitionId: '/providers/Microsoft.Authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c' // Contributor'
    principalType: 'ServicePrincipal'
  }
}

resource aks 'Microsoft.ContainerService/managedClusters@2022-04-01' = {
  name: 'mesh-demo-aks'
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${aksIdentity.id}': {}
    }
  }
  properties: {
    dnsPrefix: 'mesh-demo-aks'
    kubernetesVersion: '1.23.8'
    networkProfile: {
      networkPlugin: 'azure'
      serviceCidr: '192.168.0.0/22'
      dnsServiceIP: '192.168.0.10'
      dockerBridgeCidr: '172.16.0.0/22'
      outboundType: 'loadBalancer'
    }
    agentPoolProfiles: [
      {
        name: 'agentpool1'
        count: 3
        vmSize: 'Standard_B2ms'
        osType: 'Linux'
        vnetSubnetID: subnetId
        type: 'VirtualMachineScaleSets'
        mode: 'System'
        availabilityZones: [
          '1', '2', '3'
        ]
      }
    ]
  }
  dependsOn: [
    aksIdentityRbac
  ]
}

resource fluxExtension 'Microsoft.KubernetesConfiguration/extensions@2022-03-01' = {
  scope: aks
  name: 'flux'
  properties: {
    extensionType: 'Microsoft.Flux'
    releaseTrain: 'Stable'
    scope: {
      cluster: {
        releaseNamespace: 'flux-system'
      }
    }
    configurationSettings: {
      'helm-controller.enabled': 'true'
      'source-controller.enabled': 'true'
      'kustomize-controller.enabled': 'true'
      'notification-controller.enabled': 'true'
      'image-automation-controller.enabled': 'true'
      'image-reflector-controller.enabled': 'true'
    }
  }
}

resource fluxConfiguration 'Microsoft.KubernetesConfiguration/fluxConfigurations@2022-03-01' = {
  scope: aks
  name: 'flux'
  properties: {
    namespace: 'flux-system'
    scope: 'cluster'
    sourceKind: 'GitRepository'
    gitRepository: {
      repositoryRef: {
        branch: 'main'
      }
      syncIntervalInSeconds: 600
      timeoutInSeconds: 600
      url: 'https://github.com/tkubica12/azure-workshops'
    }
    kustomizations: {
      mydemo: {
        path: '/d-chaos-studio/kubernetes'
        timeoutInSeconds: 180
        syncIntervalInSeconds: 180
        retryIntervalInSeconds: 180
        force: true
        prune: true
        dependsOn: []
      }
    }
  }
  dependsOn: [
    fluxExtension
  ]
}

// Chaos studio
resource chaosTargetAks 'Microsoft.Chaos/targets@2021-09-15-preview' = {
  scope: aks
  name: 'microsoft-azurekubernetesservicechaosmesh'
  properties: {}
}

resource NetworkChaos 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: aks
  name: 'microsoft-azurekubernetesservicechaosmesh/NetworkChaos-2.1'
  dependsOn: [
    chaosTargetAks
  ]
}

resource IOChaos 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: aks
  name: 'microsoft-azurekubernetesservicechaosmesh/IOChaos-2.1'
  dependsOn: [
    chaosTargetAks
  ]
}

resource KernelChaos 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: aks
  name: 'microsoft-azurekubernetesservicechaosmesh/KernelChaos-2.1'
  dependsOn: [
    chaosTargetAks
  ]
}

resource PodChaos 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: aks
  name: 'microsoft-azurekubernetesservicechaosmesh/PodChaos-2.1'
  dependsOn: [
    chaosTargetAks
  ]
}

resource StressChaos 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: aks
  name: 'microsoft-azurekubernetesservicechaosmesh/StressChaos-2.1'
  dependsOn: [
    chaosTargetAks
  ]
}

resource HTTPChaos 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: aks
  name: 'microsoft-azurekubernetesservicechaosmesh/HTTPChaos-2.1'
  dependsOn: [
    chaosTargetAks
  ]
}

resource DNSChaos 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: aks
  name: 'microsoft-azurekubernetesservicechaosmesh/DNSChaos-2.1'
  dependsOn: [
    chaosTargetAks
  ]
}

resource TimeChaos 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: aks
  name: 'microsoft-azurekubernetesservicechaosmesh/TimeChaos-2.1'
  dependsOn: [
    chaosTargetAks
  ]
}


// Outputs
output aksId string = aks.id
