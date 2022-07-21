/*
  This module deploys Azure VM with Linux and Chaos Studio onboarded.
  This includes:
    - Assigning identity
    - Installing Chaos agent
    - Onboarding VM as service and agent-based target
    - Enabling capabilities
    - TBD -> creating and onboarding NSG
*/

param vmName string
param zone string
param chaosIdentityId string
param chaosIdentityClientId string
param chaosIdentityTenantId string
param subnetId string
param diagnosticsBlobUri string
param appInsightsKey string
param location string

// NIC
resource nic 'Microsoft.Network/networkInterfaces@2022-01-01' = {
  name: '${vmName}-nic'
  location: location
  properties: {
    ipConfigurations: [
      {
        name: 'ipconfig1'
        properties: {
          subnet: {
            id: subnetId
          }
        }
      }
    ]
    networkSecurityGroup: {
      id: nsg.id
    }
  }
}

// NSG
resource nsg 'Microsoft.Network/networkSecurityGroups@2022-01-01' = {
  name: '${vmName}-nsg'
  location: location
  properties: {}
}

// Virtual Machine
resource vm 'Microsoft.Compute/virtualMachines@2022-03-01' = {
  name: vmName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${chaosIdentityId}': {}
    }
  }
  zones: [
    zone
  ]
  properties: {
    hardwareProfile: {
      vmSize: 'Standard_B1s'
    }
    diagnosticsProfile: {
      bootDiagnostics: {
        enabled: true
        storageUri: diagnosticsBlobUri
      }
    }
    networkProfile: {
      networkInterfaces: [
        {
          id: nic.id
        }
      ]
    }
    osProfile: {
      computerName: vmName
      adminUsername: 'tomas'
      adminPassword: 'Azure12345678'
      linuxConfiguration: {
        disablePasswordAuthentication: false
      }
      customData: base64('#!/bin/bash\napt update && apt install -y nginx stress-ng\n')
    }
    storageProfile: {
      imageReference: {
        publisher: 'Canonical'
        offer: 'UbuntuServer'
        sku: '18.04-LTS'
        version: 'latest'
      }
      osDisk: {
        name: '${vmName}-osdisk1'
        createOption: 'FromImage'
        osType: 'Linux'
        managedDisk: {
          storageAccountType: 'Standard_LRS'
        }
      }
    }
  }
}

resource chaosExtension 'Microsoft.Compute/virtualMachines/extensions@2022-03-01' = {
  name: 'ChaosAgent'
  parent: vm
  location: location
  properties: {
    publisher: 'Microsoft.Azure.Chaos'
    type: 'ChaosLinuxAgent'
    autoUpgradeMinorVersion: true
    enableAutomaticUpgrade: false
    typeHandlerVersion: '1.0'
    settings: {
      profile: chaosTargetAgentVm1.properties.agentProfileId
      'auth.msi.clientid': chaosIdentityClientId
      appinsightskey: appInsightsKey
    }
  }
}

// Chaos - VM via service
resource chaosTargetVm1 'Microsoft.Chaos/targets@2021-09-15-preview' = {
  scope: vm
  name: 'microsoft-virtualmachine'
  properties: {}
}

resource shutDown 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: vm
  name: 'microsoft-virtualmachine/Shutdown-1.0'
  dependsOn: [
    chaosTargetVm1
  ]
}

// Chaos - VM via agent
resource chaosTargetAgentVm1 'Microsoft.Chaos/targets@2021-09-15-preview' = {
  scope: vm
  name: 'Microsoft-Agent'
  properties: {
    identities: [
      {
        type: 'AzureManagedIdentity'
        clientId: chaosIdentityClientId
        tenantId: chaosIdentityTenantId
      }
    ]
  }
}

resource cpuPressure 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: vm
  name: 'Microsoft-Agent/CPUPressure-1.0'
  dependsOn: [
    chaosTargetAgentVm1
  ]
}

resource pMemoryPressure 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: vm
  name: 'Microsoft-Agent/PhysicalMemoryPressure-1.0'
  dependsOn: [
    chaosTargetAgentVm1
  ]
}

resource vMemoryPressue 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: vm
  name: 'Microsoft-Agent/VirtualMemoryPressure-1.0'
  dependsOn: [
    chaosTargetAgentVm1
  ]
}

resource diskIoPressure 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: vm
  name: 'Microsoft-Agent/DiskIOPressure-1.0'
  dependsOn: [
    chaosTargetAgentVm1
  ]
}

resource linuxDiskIoPressure 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: vm
  name: 'Microsoft-Agent/LinuxDiskIOPressure-1.0'
  dependsOn: [
    chaosTargetAgentVm1
  ]
}

resource stopService 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: vm
  name: 'Microsoft-Agent/StopService-1.0'
  dependsOn: [
    chaosTargetAgentVm1
  ]
}

resource timeChange 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: vm
  name: 'Microsoft-Agent/TimeChange-1.0'
  dependsOn: [
    chaosTargetAgentVm1
  ]
}

resource killProcess 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: vm
  name: 'Microsoft-Agent/KillProcess-1.0'
  dependsOn: [
    chaosTargetAgentVm1
  ]
}

resource networkLatency 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: vm
  name: 'Microsoft-Agent/NetworkLatency-1.0'
  dependsOn: [
    chaosTargetAgentVm1
  ]
}

resource networkDisconnect 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: vm
  name: 'Microsoft-Agent/NetworkDisconnect-1.0'
  dependsOn: [
    chaosTargetAgentVm1
  ]
}

resource networkDisconnectViaFw 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: vm
  name: 'Microsoft-Agent/NetworkDisconnectViaFirewall-1.0'
  dependsOn: [
    chaosTargetAgentVm1
  ]
}

resource stressNg 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: vm
  name: 'Microsoft-Agent/StressNg-1.0'
  dependsOn: [
    chaosTargetAgentVm1
  ]
}

resource dnsFailure 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: vm
  name: 'Microsoft-Agent/DnsFailure-1.0'
  dependsOn: [
    chaosTargetAgentVm1
  ]
}

// Chaos - NSG
resource chaosTargetNsg 'Microsoft.Chaos/targets@2021-09-15-preview' = {
  scope: nsg
  name: 'microsoft-networksecuritygroup'
  properties: {}
}

resource securityRule 'Microsoft.Chaos/targets/capabilities@2021-09-15-preview' = {
  scope: nsg
  name: 'microsoft-networksecuritygroup/SecurityRule-1.0'
  dependsOn: [
    chaosTargetNsg
  ]
}

// Outputs
output vmId string = vm.id
