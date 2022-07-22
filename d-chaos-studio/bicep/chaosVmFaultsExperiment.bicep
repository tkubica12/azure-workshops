/*
  This module injects agent-based faults to VMs
  - Network latency
  - CPU stress
  - Disk IO stress
*/

param linuxVm1Id string
param linuxVm2Id string
param windowsVm1Id string
param windowsVm2Id string
param chaosIdentityId string
param chaosIdentityClientId string
param chaosIdentityTenantId string
param location string

// Experiment
resource vmFaultsExperiment 'Microsoft.Chaos/experiments@2021-09-15-preview' = {
  name: 'vmFaultsExperiment'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    selectors: [
      {
        type: 'List'
        id: 'linux-vms-zone1'
        targets: [
          {
            type: 'ChaosTarget'
            id: '${linuxVm1Id}/providers/Microsoft.Chaos/targets/microsoft-agent'
          }
        ]
      }
      {
        type: 'List'
        id: 'linux-vms-zone2'
        targets: [
          {
            type: 'ChaosTarget'
            id: '${linuxVm2Id}/providers/Microsoft.Chaos/targets/microsoft-agent'
          }
        ]
      }
      {
        type: 'List'
        id: 'windows-vms-zone1'
        targets: [
          {
            type: 'ChaosTarget'
            id: '${windowsVm1Id}/providers/Microsoft.Chaos/targets/microsoft-agent'
          }
        ]
      }
      {
        type: 'List'
        id: 'windows-vms-zone2'
        targets: [
          {
            type: 'ChaosTarget'
            id: '${windowsVm2Id}/providers/Microsoft.Chaos/targets/microsoft-agent'
          }
        ]
      }
    ]
    steps: [
      {
        name: 'Inject faults into VMs'
        branches: [
          {
            name: 'Network latency in Windows VM 1'
            actions: [
              {
                type: 'continuous'
                selectorId: 'windows-vms-zone1'
                name: 'urn:csci:microsoft:agent:networkLatency/1.0'
                duration: 'PT5M'
                parameters: [
                  {
                    key: 'latencyInMilliseconds'
                    value: '500'
                  }
                  {
                    key: 'destinationFilters'
                    value: '[ { "address": "10.100.0.0", "subnetMask": "255.255.0.0", "portLow":80, "portHigh":80 } ]'
                  }
                ]
              }
            ]
          }
          {
            name: 'CPU stress in Windows VM 2'
            actions: [
              {
                type: 'continuous'
                selectorId: 'windows-vms-zone2'
                name: 'urn:csci:microsoft:agent:cpuPressure/1.0'
                duration: 'PT5M'
                parameters: [
                  {
                    key: 'pressureLevel'
                    value: '90'
                  }
                ]
              }
            ]
          }
          {
            name: 'Disk IO stress in Linux VM 1'
            actions: [
              {
                type: 'continuous'
                selectorId: 'linux-vms-zone1'
                name: 'urn:csci:microsoft:agent:linuxDiskIOPressure/1.0'
                duration: 'PT5M'
                parameters: [
                  {
                    key: 'workerCount'
                    value: '10'
                  }
                  {
                    key: 'fileSizePerWorker'
                    value: '256m'
                  }
                  {
                    key: 'blockSize'
                    value: '4k'
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}

// RBAC on resource group
resource vmFaultsExperimentRbac 'Microsoft.Authorization/roleAssignments@2020-10-01-preview' = {
  name: guid('vmFaultsExperimentRbac')
  scope: resourceGroup()
  properties: {
    principalId: vmFaultsExperiment.identity.principalId
    roleDefinitionId: '/providers/Microsoft.Authorization/roleDefinitions/acdd72a7-3385-48ef-bd42-f606fba81ae7' // Reader
    principalType: 'ServicePrincipal'
  }
}
