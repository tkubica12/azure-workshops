/*
  This module implements VM shutdown experiment
  - Randomly shut one of paired VMs - 5 minutes for Linux node, 10 minutes for Windows node
  - Wait 5 minutes so app can reconverge after failure
  - Again randomly shut one of paired VMs - 5 minutes for Linux node, 10 minutes for Windows node
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
resource vmShutdownExperiment 'Microsoft.Chaos/experiments@2021-09-15-preview' = {
  name: 'vmShutdownExperiment'
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
            id: '${linuxVm1Id}/providers/Microsoft.Chaos/targets/microsoft-virtualmachine'
          }
        ]
      }
      {
        type: 'List'
        id: 'linux-vms-zone2'
        targets: [
          {
            type: 'ChaosTarget'
            id: '${linuxVm2Id}/providers/Microsoft.Chaos/targets/microsoft-virtualmachine'
          }
        ]
      }
      {
        type: 'List'
        id: 'windows-vms-zone1'
        targets: [
          {
            type: 'ChaosTarget'
            id: '${windowsVm1Id}/providers/Microsoft.Chaos/targets/microsoft-virtualmachine'
          }
        ]
      }
      {
        type: 'List'
        id: 'windows-vms-zone2'
        targets: [
          {
            type: 'ChaosTarget'
            id: '${windowsVm2Id}/providers/Microsoft.Chaos/targets/microsoft-virtualmachine'
          }
        ]
      }
    ]
    steps: [
      {
        name: 'Shutdown VMs in zone 1'
        branches: [
          {
            name: 'Force-shutdown Linux VM in zone 1 for 2 minutes'
            actions: [
              {
                type: 'continuous'
                selectorId: 'linux-vms-zone1'
                name: 'urn:csci:microsoft:virtualMachine:shutdown/1.0'
                duration: 'PT2M'
                parameters: [
                  {
                    key: 'abruptShutdown'
                    value: 'true'
                  }
                ]
              }
            ]
          }
          {
            name: 'Force-shutdown Windows VM in zone 1 for 3 minutes'
            actions: [
              {
                type: 'continuous'
                selectorId: 'windows-vms-zone1'
                name: 'urn:csci:microsoft:virtualMachine:shutdown/1.0'
                duration: 'PT3M'
                parameters: [
                  {
                    key: 'abruptShutdown'
                    value: 'true'
                  }
                ]
              }
            ]
          }
        ]
      }
      {
        name: 'Wait for 3 minutes'
        branches: [
          {
            name: 'Wait for 3 minutes'
            actions: [
              {
                type: 'delay'
                name: 'urn:csci:microsoft:chaosStudio:TimedDelay/1.0'
                duration: 'PT3M'
              }
            ]
          }
        ]
      }
      {
        name: 'Shutdown VMs in zone 2'
        branches: [
          {
            name: 'Force-shutdown Linux VM in zone 2 for 2 minutes'
            actions: [
              {
                type: 'continuous'
                selectorId: 'linux-vms-zone2'
                name: 'urn:csci:microsoft:virtualMachine:shutdown/1.0'
                duration: 'PT2M'
                parameters: [
                  {
                    key: 'abruptShutdown'
                    value: 'true'
                  }
                ]
              }
            ]
          }
          {
            name: 'Force-shutdown Windows VM in zone 2 for 3 minutes'
            actions: [
              {
                type: 'continuous'
                selectorId: 'windows-vms-zone2'
                name: 'urn:csci:microsoft:virtualMachine:shutdown/1.0'
                duration: 'PT3M'
                parameters: [
                  {
                    key: 'abruptShutdown'
                    value: 'true'
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
resource shutdownExperimentRbac 'Microsoft.Authorization/roleAssignments@2020-10-01-preview' = {
  name: guid('shutdownExperimentRbac')
  scope: resourceGroup()
  properties: {
    principalId: vmShutdownExperiment.identity.principalId
    roleDefinitionId: '/providers/Microsoft.Authorization/roleDefinitions/9980e02c-c2be-4d73-94e8-173b1dc7cf3c' // Virtual Machine Contributor
  }
}
