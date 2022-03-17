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

output envId string = env.id
