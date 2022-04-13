param prefix string
param envId string

@secure()
param password string

var location = resourceGroup().location

// Get reference to existing registry
resource registry 'Microsoft.ContainerRegistry/registries@2021-09-01' existing = {
  name: prefix
}

// Web component
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
        targetPort: 80
      }
    }
    template: {
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

// API component
resource api 'Microsoft.App/containerApps@2022-01-01-preview' = {
  name: '${prefix}-api'
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
        {
          name: 'psql-connection-string'
          value: 'jdbc:postgresql://${prefix}-db.postgres.database.azure.com:5432/todo?user=psqladmin&password=${password}&ssl=true'
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
      }
    }
    template: {
      containers: [
        {
          image: '${prefix}.azurecr.io/api:v1'
          name: 'api'
          env: [
            {
              name: 'POSTGRESQL_URL'
              secretRef: 'psql-connection-string'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 1
      }
    }
  }
}


// Azure Database for PostgreSQL
resource dbServer 'Microsoft.DBforPostgreSQL/flexibleServers@2021-06-01' = {
  name: '${prefix}-db'
  location: location
  sku: {
    name: 'Standard_B1ms'
    tier: 'Burstable'
  }
  properties: {
    administratorLogin: 'psqladmin'
    administratorLoginPassword: password
    version: '13'
    storage: {
      storageSizeGB: 32
    }
  }
}

resource dbFirewall 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2021-06-01' = {
  parent: dbServer
  name: 'allowAllAzureServices'
  properties: {
    endIpAddress: '0.0.0.0'
    startIpAddress: '0.0.0.0'
  }
}

resource dbTodo 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2021-06-01' = {
  parent: dbServer
  name: 'todo'
}

// Front Door
resource fd 'Microsoft.Cdn/profiles@2021-06-01' = {
  name: '${prefix}-fd'
  location: 'Global'
  sku: {
    name: 'Standard_AzureFrontDoor'
  }
  kind: 'frontdoor'
  properties: {
    originResponseTimeoutSeconds: 60
  }
}

resource fdEndpoint 'Microsoft.Cdn/profiles/afdEndpoints@2021-06-01' = {
  parent: fd
  name: 'todo'
  location: 'Global'
  properties: {
    enabledState: 'Enabled'
  }
}

resource apiOriginGroup 'Microsoft.Cdn/profiles/originGroups@2021-06-01' = {
  parent: fd
  name: 'api'
  properties: {
    loadBalancingSettings: {
      sampleSize: 4
      successfulSamplesRequired: 3
      additionalLatencyInMilliseconds: 50
    }
    healthProbeSettings: {
      probePath: '/'
      probeRequestType: 'HEAD'
      probeProtocol: 'Https'
      probeIntervalInSeconds: 100
    }
    sessionAffinityState: 'Disabled'
  }
}

resource webOriginGroup 'Microsoft.Cdn/profiles/originGroups@2021-06-01' = {
  parent: fd
  name: 'web'
  properties: {
    loadBalancingSettings: {
      sampleSize: 4
      successfulSamplesRequired: 3
      additionalLatencyInMilliseconds: 50
    }
    healthProbeSettings: {
      probePath: '/'
      probeRequestType: 'HEAD'
      probeProtocol: 'Https'
      probeIntervalInSeconds: 100
    }
    sessionAffinityState: 'Disabled'
  }
}

resource apiOrigin 'Microsoft.Cdn/profiles/originGroups/origins@2021-06-01' = {
  parent: apiOriginGroup
  name: 'api'
  properties: {
    hostName: api.properties.configuration.ingress.fqdn
    httpPort: 80
    httpsPort: 443
    originHostHeader: api.properties.configuration.ingress.fqdn
    priority: 1
    weight: 1000
    enabledState: 'Enabled'
    enforceCertificateNameCheck: true
  }
}

resource webOrigin 'Microsoft.Cdn/profiles/originGroups/origins@2021-06-01' = {
  parent: webOriginGroup
  name: 'web'
  properties: {
    hostName: web.properties.configuration.ingress.fqdn
    httpPort: 80
    httpsPort: 443
    originHostHeader: web.properties.configuration.ingress.fqdn
    priority: 1
    weight: 1000
    enabledState: 'Enabled'
    enforceCertificateNameCheck: true
  }
}

resource apiRoute 'Microsoft.Cdn/profiles/afdEndpoints/routes@2021-06-01' = {
  parent: fdEndpoint
  name: 'api'
  properties: {
    customDomains: []
    originGroup: {
      id: apiOriginGroup.id
    }
    ruleSets: []
    supportedProtocols: [
      'Http'
      'Https'
    ]
    patternsToMatch: [
      '/api/todo'
    ]
    forwardingProtocol: 'HttpsOnly'
    linkToDefaultDomain: 'Enabled'
    httpsRedirect: 'Enabled'
    enabledState: 'Enabled'
  }
  dependsOn: [
    apiOrigin
  ]
}

resource webRoute 'Microsoft.Cdn/profiles/afdEndpoints/routes@2021-06-01' = {
  parent: fdEndpoint
  name: 'web'
  properties: {
    customDomains: []
    originGroup: {
      id: webOriginGroup.id
    }
    ruleSets: []
    supportedProtocols: [
      'Http'
      'Https'
    ]
    patternsToMatch: [
      '/*'
    ]
    forwardingProtocol: 'MatchRequest'
    linkToDefaultDomain: 'Enabled'
    httpsRedirect: 'Enabled'
    enabledState: 'Enabled'
  }
  dependsOn: [
    webOrigin
  ]
}

// Event generator
resource eventgenerator 'Microsoft.App/containerApps@2022-01-01-preview' = {
  name: '${prefix}-eventgenerator'
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
        targetPort: 80
      }
      dapr: {
        enabled: true
        appPort: 80
        appProtocol: 'grpc'
        appId: '${prefix}-eventgenerator'
      }
    }
    template: {
      containers: [
        {
          image: '${prefix}.azurecr.io/event-generator:v1'
          name: 'eventgenerator'
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 1
      }
    }
  }
}

// Event processor
resource eventprocessor 'Microsoft.App/containerApps@2022-01-01-preview' = {
  name: '${prefix}-eventprocessor'
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
      // ingress: {
      //   external: true
      //   targetPort: 80
      // }
      dapr: {
        enabled: true
        appPort: 80
        appProtocol: 'grpc'
        appId: '${prefix}-eventgenerator'
      }
    }
    template: {
      containers: [
        {
          image: '${prefix}.azurecr.io/event-processor:v1'
          name: 'eventgenerator'
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 5
      }
    }
  }
}

