/*
  This module implements couple of AKS experiments
  - Pod killer and failure injection
  - Stress
  - Network discruption
  - API disruption
*/

param aksId string
param location string

// Pod experiments
resource podExperiments 'Microsoft.Chaos/experiments@2021-09-15-preview' = {
  name: 'podExperiments'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    selectors: [
      {
        type: 'List'
        id: 'aks'
        targets: [
          {
            type: 'ChaosTarget'
            id: '${aksId}/providers/Microsoft.Chaos/targets/microsoft-azurekubernetesservicechaosmesh'
          }
        ]
      }
    ]
    steps: [
      {
        name: 'Kill random pod in default namespace'
        branches: [
          {
            name: 'Pod killer'
            actions: [
              {
                type: 'continuous'
                selectorId: 'aks'
                name: 'urn:csci:microsoft:azureKubernetesServiceChaosMesh:podChaos/2.1'
                duration: 'PT10S'
                parameters: [
                  {
                    key: 'jsonSpec'
                    value: '{"action":"pod-kill","mode":"one","duration":"10s","selector":{"namespaces":["default"]}}'
                  }
                ]
              }
            ]
          }
        ]
      }
      {
        name: 'Kill another random pod in default namespace'
        branches: [
          {
            name: 'Pod killer'
            actions: [
              {
                type: 'continuous'
                selectorId: 'aks'
                name: 'urn:csci:microsoft:azureKubernetesServiceChaosMesh:podChaos/2.1'
                duration: 'PT10S'
                parameters: [
                  {
                    key: 'jsonSpec'
                    value: '{"action":"pod-kill","mode":"one","duration":"10s","selector":{"namespaces":["default"]}}'
                  }
                ]
              }
            ]
          }
        ]
      }
      {
        name: 'Kill another random pod in default namespace'
        branches: [
          {
            name: 'Pod killer'
            actions: [
              {
                type: 'continuous'
                selectorId: 'aks'
                name: 'urn:csci:microsoft:azureKubernetesServiceChaosMesh:podChaos/2.1'
                duration: 'PT10S'
                parameters: [
                  {
                    key: 'jsonSpec'
                    value: '{"action":"pod-kill","mode":"one","duration":"10s","selector":{"namespaces":["default"]}}'
                  }
                ]
              }
            ]
          }
        ]
      }
      {
        name: 'Fail one pod in myapp1'
        branches: [
          {
            name: 'Pod failure in myapp1'
            actions: [
              {
                type: 'continuous'
                selectorId: 'aks'
                name: 'urn:csci:microsoft:azureKubernetesServiceChaosMesh:podChaos/2.1'
                duration: 'PT2M'
                parameters: [
                  {
                    key: 'jsonSpec'
                    value: '{"action":"pod-failure","mode":"one","selector":{"namespaces":["default"],"labelSelectors":{"app":"myapp1"}}}'
                  }
                ]
              }
            ]
          }
          {
            name: 'Pod failure in myapp2'
            actions: [
              {
                type: 'continuous'
                selectorId: 'aks'
                name: 'urn:csci:microsoft:azureKubernetesServiceChaosMesh:podChaos/2.1'
                duration: 'PT2M'
                parameters: [
                  {
                    key: 'jsonSpec'
                    value: '{"action":"pod-failure","mode":"one","selector":{"namespaces":["default"],"labelSelectors":{"app":"myapp2"}}}'
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
resource podKillerRbac 'Microsoft.Authorization/roleAssignments@2020-10-01-preview' = {
  name: guid('podKillerRbac')
  scope: resourceGroup()
  properties: {
    principalId: podExperiments.identity.principalId
    roleDefinitionId: '/providers/Microsoft.Authorization/roleDefinitions/0ab0b1a8-8aac-4efd-b8c2-3ee1fb270be8' // Azure Kubernetes Service Cluster Admin Role
    principalType: 'ServicePrincipal'
  }
}
