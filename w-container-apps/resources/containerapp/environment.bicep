var location = resourceGroup().location

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

resource env 'Microsoft.App/managedEnvironments@2022-01-01-preview' = {
  name: '${uniqueString(resourceGroup().id)}'
  location: location
  properties: {
    type: 'managed'
    internalLoadBalancerEnabled: false
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: monitor.properties.customerId
        sharedKey: monitor.listKeys().primarySharedKey
      }
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
        secretRef: 'sbConnectionString'
      }
    ]
    secrets: [
      {
        name: 'sbConnectionString'
        value: listKeys(sbAuthorization.id, sbAuthorization.apiVersion).primaryConnectionString
      }
    ]
    scopes: [
      'something'
    ]
  }
}


output envId string = env.id
