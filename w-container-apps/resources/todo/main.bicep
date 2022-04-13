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

// Azure Front Door
resource fd 'Microsoft.Network/frontdoors@2020-05-01' = {
  name: prefix
  location: 'Global'
  properties: {
    friendlyName: prefix
    enabledState: 'Enabled'
    healthProbeSettings: [
      {
        name: 'probe'
        properties: {
          path: '/'
          protocol: 'Https'
          intervalInSeconds: 30
          healthProbeMethod: 'HEAD'
          enabledState: 'Enabled'
        }
      }
    ]
    loadBalancingSettings: [
      {
        name: 'lbSettings'
        properties: {
          sampleSize: 4
          successfulSamplesRequired: 2
          additionalLatencyMilliseconds: 0
        }
      }
    ]
    frontendEndpoints: [
      {
        name: '${prefix}-azurefd-net'
        properties: {
          hostName: '${prefix}.azurefd.net'
          sessionAffinityEnabledState: 'Disabled'
        }
      }
    ]
    backendPools: [
      {
        name: 'web'
        properties: {
          backends: [
            {
              address: web.properties.configuration.ingress.fqdn
              enabledState: 'Enabled'
              httpPort: 80
              httpsPort: 443
              priority: 1
              weight: 50
              backendHostHeader: web.properties.configuration.ingress.fqdn
            }
          ]
          loadBalancingSettings: {
            id: '${resourceGroup().id}/providers/Microsoft.Network/frontdoors/${prefix}/loadBalancingSettings/lbSettings'
          }
          healthProbeSettings: {
            id: '${resourceGroup().id}/providers/Microsoft.Network/frontdoors/${prefix}/healthProbeSettings/probe'
          }
        }
      }
      {
        name: 'api'
        properties: {
          backends: [
            {
              address: api.properties.configuration.ingress.fqdn
              enabledState: 'Enabled'
              httpPort: 80
              httpsPort: 443
              priority: 1
              weight: 50
              backendHostHeader: api.properties.configuration.ingress.fqdn
            }
          ]
          loadBalancingSettings: {
            id: '${resourceGroup().id}/providers/Microsoft.Network/frontdoors/${prefix}/loadBalancingSettings/lbSettings'
          }
          healthProbeSettings: {
            id: '${resourceGroup().id}/providers/Microsoft.Network/frontdoors/${prefix}/healthProbeSettings/probe'
          }
        }
      }
    ]
    routingRules: [
      {
        name: 'web'
        properties: {
          frontendEndpoints: [
            {
              id: '${resourceGroup().id}/providers/Microsoft.Network/frontdoors/${prefix}/frontendEndpoints/${prefix}-azurefd-net'
            }
          ]
          acceptedProtocols: [
            'Http'
            'Https'
          ]
          patternsToMatch: [
            '/*'
          ]
          enabledState: 'Enabled'
          routeConfiguration: {
            '@odata.type': '#Microsoft.Azure.FrontDoor.Models.FrontdoorForwardingConfiguration'
            customForwardingPath: null
            forwardingProtocol: 'HttpsOnly'
            backendPool: {
              id: '${resourceGroup().id}/providers/Microsoft.Network/frontdoors/${prefix}/backendPools/web'
            }
            cacheConfiguration: null
          }
        }
      }
      {
        name: 'api'
        properties: {
          frontendEndpoints: [
            {
              id: '${resourceGroup().id}/providers/Microsoft.Network/frontdoors/${prefix}/frontendEndpoints/${prefix}-azurefd-net'
            }
          ]
          acceptedProtocols: [
            'Http'
            'Https'
          ]
          patternsToMatch: [
            '/api/*'
          ]
          enabledState: 'Enabled'
          routeConfiguration: {
            '@odata.type': '#Microsoft.Azure.FrontDoor.Models.FrontdoorForwardingConfiguration'
            customForwardingPath: null
            forwardingProtocol: 'HttpsOnly'
            backendPool: {
              id: '${resourceGroup().id}/providers/Microsoft.Network/frontdoors/${prefix}/backendPools/api'
            }
            cacheConfiguration: null
          }
        }
      }
    ]
    backendPoolsSettings: {
      enforceCertificateNameCheck: 'Enabled'
      sendRecvTimeoutSeconds: 30
    }
  }
}

// Event generator
resource web 'Microsoft.App/containerApps@2022-01-01-preview' = {
  name: '${prefix}-generator'
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
        appId: 'event-generator'
        components: [
          {
            name: 'pubsub'
            type: 'pubsub.azure.servicebus'
            version: 'v1'
            metadata: [
              {
                name: 'connectionString'
                value: listKeys(sbAuthorization.id, sbAuthorization.apiVersion).primaryConnectionString
              }
            ]
          }
        ]
      }
    }
    template: {
      containers: [
        {
          image: '${prefix}.azurecr.io/event-generator:v1'
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
