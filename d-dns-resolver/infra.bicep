var location = resourceGroup().location

// Networks
resource azureServicesVnet 'Microsoft.Network/virtualNetworks@2021-08-01' = {
  name: 'azureServicesVnet'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.1.0.0/16'
      ]
    }
    subnets: [
      {
        name: 'vm'
        properties: {
          addressPrefix: '10.1.0.0/24'
          privateEndpointNetworkPolicies: 'Disabled'
        }
      }
      {
        name: 'dns-in'
        properties: {
          addressPrefix: '10.1.1.0/24'
          delegations: [
            {
              name: 'dnsResolverLink'
              properties: {
                serviceName: 'Microsoft.Network/dnsResolvers'
              }
            }
          ]
        }
      }
      {
        name: 'dns-out'
        properties: {
          addressPrefix: '10.1.2.0/24'
          delegations: [
            {
              name: 'dnsResolverLink'
              properties: {
                serviceName: 'Microsoft.Network/dnsResolvers'
              }
            }
          ]
        }
      }
    ]
  }
}

resource onpremVnet 'Microsoft.Network/virtualNetworks@2021-08-01' = {
  name: 'onpremVnet'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.99.0.0/16'
      ]
    }
    subnets: [
      {
        name: 'vm'
        properties: {
          addressPrefix: '10.99.0.0/24'
        }
      }
      {
        name: 'dns'
        properties: {
          addressPrefix: '10.99.1.0/24'
        }
      }
    ]
  }
}

resource azureSpokeVnet 'Microsoft.Network/virtualNetworks@2021-08-01' = {
  name: 'azureSpokeVnet'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.5.0.0/16'
      ]
    }
    dhcpOptions: {
      dnsServers: [
        azureDnsResolverIn.properties.ipConfigurations[0].privateIpAddress
      ]
    }
    subnets: [
      {
        name: 'vm'
        properties: {
          addressPrefix: '10.5.0.0/24'
        }
      }
    ]
  }
}

// Simulate VPN connection using VNET peering
resource peerAzureOnprem 'Microsoft.Network/virtualNetworks/virtualNetworkPeerings@2021-08-01' = {
  name: 'peerAzureOnprem'
  parent: azureServicesVnet
  properties: {
    remoteVirtualNetwork: {
      id: onpremVnet.id
    }
    allowForwardedTraffic: true
    allowVirtualNetworkAccess: true
  }
}

resource peerOnpremAzure 'Microsoft.Network/virtualNetworks/virtualNetworkPeerings@2021-08-01' = {
  name: 'peerOnpremAzure'
  parent: onpremVnet
  properties: {
    remoteVirtualNetwork: {
      id: azureServicesVnet.id
    }
    allowForwardedTraffic: true
    allowVirtualNetworkAccess: true
  }
}

// vWAN
resource vwan 'Microsoft.Network/virtualWans@2021-08-01' = {
  name: 'vwan'
  location: location
  properties: {
    allowVnetToVnetTraffic: true
  }
}

resource vHub 'Microsoft.Network/virtualHubs@2021-08-01' = {
  name: 'vHub'
  location: location
  properties: {
   virtualWan: {
     id: vwan.id
   } 
   addressPrefix: '10.20.0.0/16'
   sku: 'Standard'
  }
}

resource azureServicesVnetToHub 'Microsoft.Network/virtualHubs/hubVirtualNetworkConnections@2021-08-01' = {
  name: 'azureServicesVnetToHub'
  parent: vHub
  properties: {
    remoteVirtualNetwork: {
      id: azureServicesVnet.id
    }
  }
}

resource azureSpokeVnetToHub 'Microsoft.Network/virtualHubs/hubVirtualNetworkConnections@2021-08-01' = {
  name: 'azureSpokeVnetToHub'
  parent: vHub
  properties: {
    remoteVirtualNetwork: {
      id: azureSpokeVnet.id
    }
  }
}

// DNS resolver
resource azureDnsResolver 'Microsoft.Network/dnsResolvers@2020-04-01-preview' = {
  name: 'azureDnsResolver'
  location: location
  properties: {
    virtualNetwork: {
      id: azureServicesVnet.id
    }
  }
}

resource azureDnsResolverIn 'Microsoft.Network/dnsResolvers/inboundEndpoints@2020-04-01-preview' = {
  name: 'azureDnsResolverIn'
  parent: azureDnsResolver
  location: location
  properties: {
    ipConfigurations: [
      {
        privateIpAllocationMethod: 'Dynamic'
        subnet: {
          id: '${azureServicesVnet.id}/subnets/dns-in'
        }
      }
    ]
  }
}

output azureDnsResolverInIp string = azureDnsResolverIn.properties.ipConfigurations[0].privateIpAddress

resource azureDnsResolverOut 'Microsoft.Network/dnsResolvers/outboundEndpoints@2020-04-01-preview' = {
  name: 'azureDnsResolverOut'
  parent: azureDnsResolver
  location: location
  properties: {
    subnet: {
      id: '${azureServicesVnet.id}/subnets/dns-out'
    }
  }
}

resource forwardingRuleSet 'Microsoft.Network/dnsForwardingRulesets@2020-04-01-preview' = {
  name: 'myForwardingRuleSet'
  location: location
  properties: {
    dnsResolverOutboundEndpoints: [
      {
        id: azureDnsResolverOut.id
      }
    ]
  }
}

resource forwardingRuleSetVnetLink 'Microsoft.Network/dnsForwardingRulesets/virtualNetworkLinks@2020-04-01-preview' = {
  name: 'myForwardingRuleSetVnetLink'
  parent: forwardingRuleSet
  properties: {
    virtualNetwork: {
      id: azureServicesVnet.id
    }
  }
}

resource forwardingRules 'Microsoft.Network/dnsForwardingRulesets/forwardingRules@2020-04-01-preview' = {
  name: 'myForwardingRules'
  parent: forwardingRuleSet
  properties: {
    domainName: 'onprem.mydomain.demo.'
    targetDnsServers: [
      {
        ipAddress: '10.99.1.10'
        port: 53
      }
    ]
  }
}

// Private DNS zone and link to all VNETs (to enable registration of records across Azure)
resource privateDns 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'azure.mydomain.demo'
  location: 'global'
}

resource privateDnsVnetLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  name: 'myPrivateDnsVnetLink'
  parent: privateDns
  location: 'global'
  properties: {
    virtualNetwork: {
      id: azureServicesVnet.id
    }
    registrationEnabled: true
  }
}

resource privateDnsVnetLinkSpoke 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  name: 'myPrivateDnsVnetLinkSpoke'
  parent: privateDns
  location: 'global'
  properties: {
    virtualNetwork: {
      id: azureSpokeVnet.id
    }
    registrationEnabled: true
  }
}

// Diagnostics storage
resource storage 'Microsoft.Storage/storageAccounts@2021-09-01' = {
  name: uniqueString(resourceGroup().id)
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}

// Cloud VM
resource cloudVmNic 'Microsoft.Network/networkInterfaces@2021-08-01' = {
  name: 'cloudVmNic'
  location: location
  properties: {
    ipConfigurations: [
      {
        name: 'ipConfig'
        properties: {
          subnet: {
            id: '${azureServicesVnet.id}/subnets/vm'
          }
          privateIPAllocationMethod: 'Dynamic'
        }
      }
    ]
  }
}

resource cloudVm 'Microsoft.Compute/virtualMachines@2021-11-01' = {
  name: 'cloudVm'
  location: location
  properties: {
    hardwareProfile: {
      vmSize: 'Standard_B1s'
    }
    storageProfile: {
      osDisk: {
        name: 'osDiskcloudVm'
        caching: 'ReadWrite'
        createOption: 'FromImage'
        managedDisk: {
          storageAccountType: 'Standard_LRS'
        }
      }
      imageReference: {
        publisher: 'Canonical'
        offer: 'UbuntuServer'
        sku: '18.04-LTS'
        version: 'latest'
      }
    }
    networkProfile: {
      networkInterfaces: [
        {
          id: cloudVmNic.id
        }
      ]
    }
    osProfile: {
      computerName: 'cloudVm'
      adminUsername: 'tomas'
      adminPassword: 'Azure12345678'
    }
    diagnosticsProfile: {
      bootDiagnostics: {
        enabled: true
        storageUri: storage.properties.primaryEndpoints.blob
      }
    }
  }
}

// Spoke VM
resource spokeVmNic 'Microsoft.Network/networkInterfaces@2021-08-01' = {
  name: 'spokeVmNic'
  location: location
  properties: {
    ipConfigurations: [
      {
        name: 'ipConfig'
        properties: {
          subnet: {
            id: '${azureSpokeVnet.id}/subnets/vm'
          }
          privateIPAllocationMethod: 'Dynamic'
        }
      }
    ]
  }
}

resource spokeVm 'Microsoft.Compute/virtualMachines@2021-11-01' = {
  name: 'spokeVm'
  location: location
  properties: {
    hardwareProfile: {
      vmSize: 'Standard_B1s'
    }
    storageProfile: {
      osDisk: {
        name: 'osDiskspokeVmNic'
        caching: 'ReadWrite'
        createOption: 'FromImage'
        managedDisk: {
          storageAccountType: 'Standard_LRS'
        }
      }
      imageReference: {
        publisher: 'Canonical'
        offer: 'UbuntuServer'
        sku: '18.04-LTS'
        version: 'latest'
      }
    }
    networkProfile: {
      networkInterfaces: [
        {
          id: spokeVmNic.id
        }
      ]
    }
    osProfile: {
      computerName: 'spokeVmNic'
      adminUsername: 'tomas'
      adminPassword: 'Azure12345678'
    }
    diagnosticsProfile: {
      bootDiagnostics: {
        enabled: true
        storageUri: storage.properties.primaryEndpoints.blob
      }
    }
  }
}

// Onprem VM
resource onpremVmNic 'Microsoft.Network/networkInterfaces@2021-08-01' = {
  name: 'onpremVmNic'
  location: location
  properties: {
    ipConfigurations: [
      {
        name: 'ipConfig'
        properties: {
          subnet: {
            id: '${onpremVnet.id}/subnets/vm'
          }
          privateIPAllocationMethod: 'Dynamic'
        }
      }
    ]
    dnsSettings: {
      dnsServers: [
        '10.99.1.10'
      ]
    }
  }
}

resource onpremVm 'Microsoft.Compute/virtualMachines@2021-11-01' = {
  name: 'onpremVm'
  location: location
  properties: {
    hardwareProfile: {
      vmSize: 'Standard_B1s'
    }
    storageProfile: {
      osDisk: {
        name: 'osDiskonpremVm'
        caching: 'ReadWrite'
        createOption: 'FromImage'
        managedDisk: {
          storageAccountType: 'Standard_LRS'
        }
      }
      imageReference: {
        publisher: 'Canonical'
        offer: 'UbuntuServer'
        sku: '18.04-LTS'
        version: 'latest'
      }
    }
    networkProfile: {
      networkInterfaces: [
        {
          id: onpremVmNic.id
        }
      ]
    }
    osProfile: {
      computerName: 'onpremVm'
      adminUsername: 'tomas'
      adminPassword: 'Azure12345678'
    }
    diagnosticsProfile: {
      bootDiagnostics: {
        enabled: true
        storageUri: storage.properties.primaryEndpoints.blob
      }
    }
  }
}

// Onprem DNS
resource onpremDnsVmNic 'Microsoft.Network/networkInterfaces@2021-08-01' = {
  name: 'onpremDnsVmNic'
  location: location
  properties: {
    ipConfigurations: [
      {
        name: 'ipConfig'
        properties: {
          subnet: {
            id: '${onpremVnet.id}/subnets/dns'
          }
          privateIPAllocationMethod: 'Static'
          privateIPAddress: '10.99.1.10'
        }
      }
    ]
  }
}

resource onpremDnsVm 'Microsoft.Compute/virtualMachines@2021-11-01' = {
  name: 'onpremDnsVm'
  location: location
  properties: {
    hardwareProfile: {
      vmSize: 'Standard_B1s'
    }
    storageProfile: {
      osDisk: {
        name: 'osDiskonpremDnsVm'
        caching: 'ReadWrite'
        createOption: 'FromImage'
        managedDisk: {
          storageAccountType: 'Standard_LRS'
        }
      }
      imageReference: {
        publisher: 'Canonical'
        offer: 'UbuntuServer'
        sku: '18.04-LTS'
        version: 'latest'
      }
    }
    networkProfile: {
      networkInterfaces: [
        {
          id: onpremDnsVmNic.id
        }
      ]
    }
    osProfile: {
      computerName: 'onpremDnsVm'
      adminUsername: 'tomas'
      adminPassword: 'Azure12345678'
    }
    diagnosticsProfile: {
      bootDiagnostics: {
        enabled: true
        storageUri: storage.properties.primaryEndpoints.blob
      }
    }
  }
}

// PaaS with private endpoint
resource service 'Microsoft.Storage/storageAccounts@2021-09-01' = {
  name: uniqueString(resourceGroup().id, 'mydemo')
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}

output serviceFqdn string = service.properties.primaryEndpoints.blob

resource storagePrivateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.blob.core.windows.net'
  location: 'global'
}

resource storagePrivateDnsZoneVnetLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  name: 'storagePrivateDnsZoneVnetLink'
  parent: storagePrivateDnsZone
  location: 'global'
  properties: {
    virtualNetwork: {
      id: azureServicesVnet.id
    }
    registrationEnabled: false
  }
}

resource privateEndpoint 'Microsoft.Network/privateEndpoints@2021-08-01' = {
  name: 'privateEndpoint'
  location: location
  properties: {
    subnet: {
      id: '${azureServicesVnet.id}/subnets/vm'
    }
    privateLinkServiceConnections: [
      {
        name: 'privateLinkServiceConnection'
        properties: {
          groupIds: [
            'blob'
          ]
          privateLinkServiceId: service.id
        }
      }
    ]
  }
}

resource privateEndpointDnsRegistration 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2021-05-01' = {
  name: 'privateEndpointDnsRegistration'
  parent: privateEndpoint
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'config1'
        properties: {
          privateDnsZoneId: storagePrivateDnsZone.id
        }
      }
    ]
  }
}
