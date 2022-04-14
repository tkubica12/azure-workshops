var location = resourceGroup().location

// Monitoring
resource monitor 'Microsoft.OperationalInsights/workspaces@2020-03-01-preview' = {
  name: '${uniqueString(resourceGroup().id)}'
  location: location
  properties: any({
    retentionInDays: 30
    features: {
      searchVersion: 1
    }
    sku: {
      name: 'PerGB2018'
    }
  })
}

// Network
resource vnet 'Microsoft.Network/virtualNetworks@2021-05-01' = {
  name: 'capp-vnet'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
    }
    subnets: [
      {
        name: 'capp-control'
        properties: {
          addressPrefix: '10.0.0.0/21'
        }
      }
      {
        name: 'capp-app'
        properties: {
          addressPrefix: '10.0.8.0/21'
        }
      }
    ]
  }
}

resource env 'Microsoft.App/managedEnvironments@2022-01-01-preview' = {
  name: '${uniqueString(resourceGroup().id)}'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: monitor.properties.customerId
        sharedKey: monitor.listKeys().primarySharedKey
      }
    }
    vnetConfiguration: {
      infrastructureSubnetId: '${vnet.id}/subnets/capp-control'
      runtimeSubnetId: '${vnet.id}/subnets/capp-app'
      internal: false
    }
  }
}

// Service Bus
resource sb 'Microsoft.ServiceBus/namespaces@2021-11-01' = {
  name: 'shared${uniqueString(resourceGroup().id)}'
  location: location
  sku: {
    name: 'Standard'
    tier: 'Standard'
  }
}

resource sbAuthorization 'Microsoft.ServiceBus/namespaces/AuthorizationRules@2017-04-01' = {
  parent: sb
  name: 'ListenSend'
  properties: {
    rights: [
      'Listen'
      'Send'
    ]
  }
}

// DAPR component for pubsub using ServiceBus
resource daprPubsub 'Microsoft.App/managedEnvironments/daprComponents@2022-01-01-preview' = {
  parent: env
  name: 'pubsub'
  properties: {
    componentType: 'pubsub.azure.servicebus'
    version: 'v1'
    metadata: [
      {
        name: 'connectionString'
        secretRef: 'sbconnectionstring'
      }
    ]
    secrets: [
      {
        name: 'sbconnectionstring'
        value: listKeys(sbAuthorization.id, sbAuthorization.apiVersion).primaryConnectionString
      }
    ]
    scopes: [
      'something'
    ]
  }
}


output envId string = env.id
