param prefix string
param envId string

var location = resourceGroup().location

resource registry 'Microsoft.ContainerRegistry/registries@2021-09-01'  existing = {
  name: prefix
}

resource web 'Microsoft.App/containerApps@2022-01-01-preview' = {
  name: '${prefix}-web'
  kind: 'containerapp'
  location: location
  properties: {
    managedEnvironmentId: envId
    configuration: {
      secrets: [
        {
          name: 'container-registry-password'
          value: registry.listCredentials().passwords[0].value
        }
      ]      
      registries: [
        {
          server: '${prefix}.azurecr.io'
          username: registry.listCredentials().username
          passwordSecretRef: 'container-registry-password'
        }
      ]
      ingress: {
        external: true
        targetPort: 8080
        traffic: [
          {
            weight: 0
            latestRevision: true
          }
          {
            weight: 100
            revisionName: '${prefix}-web--v1-rev1'
          }
        ]
      }
    }
    template: {
      revisionSuffix: 'v1-rev1'
      containers: [
        {
          image: '${prefix}.azurecr.io/web:v1'
          name: 'web'
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 1
      }
    }
  }
}
