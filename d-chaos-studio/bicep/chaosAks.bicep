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

// Pod experiments RBAC on resource group
resource podKillerRbac 'Microsoft.Authorization/roleAssignments@2020-10-01-preview' = {
  name: guid('podKillerRbac')
  scope: resourceGroup()
  properties: {
    principalId: podExperiments.identity.principalId
    roleDefinitionId: '/providers/Microsoft.Authorization/roleDefinitions/0ab0b1a8-8aac-4efd-b8c2-3ee1fb270be8' // Azure Kubernetes Service Cluster Admin Role
    principalType: 'ServicePrincipal'
  }
}

// Stress experiments
resource stressExperiments 'Microsoft.Chaos/experiments@2021-09-15-preview' = {
  name: 'stressExperiments'
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
        name: 'Generate stress'
        branches: [
          {
            name: 'High CPU usage on one of myapp1 pods'
            actions: [
              {
                type: 'continuous'
                selectorId: 'aks'
                name: 'urn:csci:microsoft:azureKubernetesServiceChaosMesh:stressChaos/2.1'
                duration: 'PT1M'
                parameters: [
                  {
                    key: 'jsonSpec'
                    value: '{"mode":"one","selector":{"namespaces":["default"],"labelSelectors":{"app":"myapp1"}},"stressors":{"cpu":{"workers":2,"load":80}}}'
                  }
                ]
              }
            ]
          }
          {
            name: 'High memory usage on one of myapp2 pods'
            actions: [
              {
                type: 'continuous'
                selectorId: 'aks'
                name: 'urn:csci:microsoft:azureKubernetesServiceChaosMesh:stressChaos/2.1'
                duration: 'PT1M'
                parameters: [
                  {
                    key: 'jsonSpec'
                    value: '{"mode":"one","selector":{"namespaces":["default"],"labelSelectors":{"app":"myapp2"}},"stressors":{"memory":{"workers":20,"size":"512MB"}}}'
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
resource stressExperimentsRbac 'Microsoft.Authorization/roleAssignments@2020-10-01-preview' = {
  name: guid('stressExperimentsRbac')
  scope: resourceGroup()
  properties: {
    principalId: stressExperiments.identity.principalId
    roleDefinitionId: '/providers/Microsoft.Authorization/roleDefinitions/0ab0b1a8-8aac-4efd-b8c2-3ee1fb270be8' // Azure Kubernetes Service Cluster Admin Role
    principalType: 'ServicePrincipal'
  }
}

// Stress experiments
resource networkExperiments 'Microsoft.Chaos/experiments@2021-09-15-preview' = {
  name: 'networkExperiments'
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
        name: 'Network and connectivity faults'
        branches: [
          {
            name: 'Added network latency myapp1'
            actions: [
              {
                type: 'continuous'
                selectorId: 'aks'
                name: 'urn:csci:microsoft:azureKubernetesServiceChaosMesh:networkChaos/2.1'
                duration: 'PT2M'
                parameters: [
                  {
                    key: 'jsonSpec'
                    value: '{"mode":"all","selector":{"namespaces":["default"],"labelSelectors":{"app":"myapp1"}},"action":"delay","delay":{"latency":"100ms","correlation":"100","jitter":"50ms"}}'
                  }
                ]
              }
            ]
          }
          {
            name: 'Inject fake responses from myapp1 in myapp2'
            actions: [
              {
                type: 'continuous'
                selectorId: 'aks'
                name: 'urn:csci:microsoft:azureKubernetesServiceChaosMesh:httpChaos/2.1'
                duration: 'PT2M'
                parameters: [
                  {
                    key: 'jsonSpec'
                    value: '{"mode":"all","selector":{"namespaces":["default"],"labelSelectors":{"app":"myapp2"}},"target":"Response","port":80,"replace":{"body":"eyJpcCI6ICJqZWpkYVRvaGxlSmVTdHJpbmcifQ=="}}'
                  }
                ]
              }
            ]
          }
          {
            name: 'Provide fake responses on DNS request to tomaskubica.cz'
            actions: [
              {
                type: 'continuous'
                selectorId: 'aks'
                name: 'urn:csci:microsoft:azureKubernetesServiceChaosMesh:dnsChaos/2.1'
                duration: 'PT2M'
                parameters: [
                  {
                    key: 'jsonSpec'
                    value: '{"mode":"all","selector":{"namespaces":["default"],"labelSelectors":{"app":"myapp1"}},"action":"random","patterns":["tomaskubica.cz"]}'
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
resource networkExperimentsRbac 'Microsoft.Authorization/roleAssignments@2020-10-01-preview' = {
  name: guid('networkExperiments')
  scope: resourceGroup()
  properties: {
    principalId: networkExperiments.identity.principalId
    roleDefinitionId: '/providers/Microsoft.Authorization/roleDefinitions/0ab0b1a8-8aac-4efd-b8c2-3ee1fb270be8' // Azure Kubernetes Service Cluster Admin Role
    principalType: 'ServicePrincipal'
  }
}
