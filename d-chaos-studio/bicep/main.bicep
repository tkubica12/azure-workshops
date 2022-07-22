var location = resourceGroup().location

// Networking
resource vnet 'Microsoft.Network/virtualNetworks@2022-01-01' = {
  name: 'chaos-vnet'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.100.0.0/16'
      ]
    }
    subnets: [
      {
        name: 'aks'
        properties: {
          addressPrefix: '10.100.0.0/22'
        }
      }
      {
        name: 'vms'
        properties: {
          addressPrefix: '10.100.4.0/24'
        }
      }
    ]
  }
}

// Monitoring and diagnostics
resource diag 'Microsoft.Storage/storageAccounts@2021-09-01' = {
  name: 'storage${uniqueString(resourceGroup().id)}'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}

resource logWorkspace 'Microsoft.OperationalInsights/workspaces@2021-06-01' = {
  name: 'logs${uniqueString(resourceGroup().id)}'
  location: location
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appinsights'
  location: location
  kind: 'Web'
  properties: {
    Application_Type: 'Web'
    WorkspaceResourceId: logWorkspace.id
  }
}

// Chaos Studio identity
resource chaosIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2022-01-31-preview' = {
  name: 'chaosidentity'
  location: location
}

resource chaosAgentsRbac 'Microsoft.Authorization/roleAssignments@2020-10-01-preview' = {
  name: guid('chaosAgentsRbac')
  scope: resourceGroup()
  properties: {
    principalId: chaosIdentity.properties.principalId
    roleDefinitionId: '/providers/Microsoft.Authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c' // Contributor, but should be custom role for Chaos upload only
  }
}

// Deploy VMs
module linuxVm1 'linuxVm.bicep' = {
  name: 'linuxVm1'
  params: {
    appInsightsKey: appInsights.properties.InstrumentationKey
    diagnosticsBlobUri: diag.properties.primaryEndpoints.blob
    chaosIdentityClientId: chaosIdentity.properties.clientId
    chaosIdentityId: chaosIdentity.id
    chaosIdentityTenantId: chaosIdentity.properties.tenantId
    location: location
    subnetId: '${vnet.id}/subnets/vms'
    vmName: 'linuxVm1'
    zone: '1'
  }
}

module linuxVm2 'linuxVm.bicep' = {
  name: 'linuxVm2'
  params: {
    appInsightsKey: appInsights.properties.InstrumentationKey
    diagnosticsBlobUri: diag.properties.primaryEndpoints.blob
    chaosIdentityClientId: chaosIdentity.properties.clientId
    chaosIdentityId: chaosIdentity.id
    chaosIdentityTenantId: chaosIdentity.properties.tenantId
    location: location
    subnetId: '${vnet.id}/subnets/vms'
    vmName: 'linuxVm2'
    zone: '2'
  }
}

module windowsVm1 'windowsVm.bicep' = {
  name: 'windowsVm1'
  params: {
    appInsightsKey: appInsights.properties.InstrumentationKey
    diagnosticsBlobUri: diag.properties.primaryEndpoints.blob
    chaosIdentityClientId: chaosIdentity.properties.clientId
    chaosIdentityId: chaosIdentity.id
    chaosIdentityTenantId: chaosIdentity.properties.tenantId
    location: location
    subnetId: '${vnet.id}/subnets/vms'
    vmName: 'windowsVm1'
    zone: '1'
  }
}

module windowsVm2 'windowsVm.bicep' = {
  name: 'windowsVm2'
  params: {
    appInsightsKey: appInsights.properties.InstrumentationKey
    diagnosticsBlobUri: diag.properties.primaryEndpoints.blob
    chaosIdentityClientId: chaosIdentity.properties.clientId
    chaosIdentityId: chaosIdentity.id
    chaosIdentityTenantId: chaosIdentity.properties.tenantId
    location: location
    subnetId: '${vnet.id}/subnets/vms'
    vmName: 'windowsVm2'
    zone: '2'
  }
}

// Kubernetes
module aks 'kubernetes.bicep' = {
  name: 'aks'
  params: {
    location: location
    subnetId: '${vnet.id}/subnets/aks'
  }
}

// Experiments
module shutdownExperiment 'chaosShutdownExperiment.bicep' = {
  name: 'shutdownExperiment'
  params: {
    chaosIdentityClientId: chaosIdentity.properties.clientId
    chaosIdentityId: chaosIdentity.id
    chaosIdentityTenantId: chaosIdentity.properties.tenantId
    location: location
    linuxVm1Id: linuxVm1.outputs.vmId
    linuxVm2Id: linuxVm2.outputs.vmId
    windowsVm1Id: windowsVm1.outputs.vmId
    windowsVm2Id: windowsVm2.outputs.vmId
  }
}

module vmFaultsExperiment 'chaosVmFaultsExperiment.bicep' = {
  name: 'vmFaultsExperiment'
  params: {
    chaosIdentityClientId: chaosIdentity.properties.clientId
    chaosIdentityId: chaosIdentity.id
    chaosIdentityTenantId: chaosIdentity.properties.tenantId
    location: location
    linuxVm1Id: linuxVm1.outputs.vmId
    linuxVm2Id: linuxVm2.outputs.vmId
    windowsVm1Id: windowsVm1.outputs.vmId
    windowsVm2Id: windowsVm2.outputs.vmId
  }
}

module aksExperiments 'chaosAks.bicep' = {
  name: 'aksExperiments'
  params: {
    aksId: aks.outputs.aksId
    location: location
  }
}

// Outputs
// output debug string = linuxVm1.outputs.vmId
// output debug2 string = chaosTargetAgentVm1.id
