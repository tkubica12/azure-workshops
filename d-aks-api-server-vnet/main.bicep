var location = resourceGroup().location

resource vnet 'Microsoft.Network/virtualNetworks@2022-01-01' = {
  name: 'myvnet'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.88.0.0/16'
      ]
    }
    subnets: [
      {
        name: 'nodes'
        properties: {
          addressPrefix: '10.88.0.0/24'
          routeTable: {
            id: routeTable.id
          }
        }
      }
      {
        name: 'apiserver'
        properties: {
          addressPrefix: '10.88.1.0/24'
          routeTable: {
            id: routeTable.id
          }
          delegations: [
            {
              name: 'apiserver'
              properties: {
                serviceName: 'Microsoft.ContainerService/managedClusters'
              }
            }
          ]
        }
      }
      {
        name: 'pods'
        properties: {
          addressPrefix: '10.88.2.0/23'
          routeTable: {
            id: routeTable.id
          }
        }
      }
      {
        name: 'AzureFirewallSubnet'
        properties: {
          addressPrefix: '10.88.4.0/24'
        }
      }
    ]
  }
}

resource routeTable 'Microsoft.Network/routeTables@2022-01-01' = {
  name: 'routeTable'
  location: location
  properties: {}
}

resource defaultRoute 'Microsoft.Network/routeTables/routes@2022-01-01' = {
  name: 'defaultRoute'
  parent: routeTable
  properties: {
    nextHopType: 'VirtualAppliance'
    addressPrefix: '0.0.0.0/0'
    nextHopIpAddress: fw.properties.ipConfigurations[0].properties.privateIPAddress
  }
}

resource fw 'Microsoft.Network/azureFirewalls@2022-01-01' = {
  name: 'myfw'
  location: location
  properties: {
    sku: {
      name: 'AZFW_VNet'
      tier: 'Standard'
    }
    ipConfigurations: [
      {
        name: 'ipconfig'
        properties: {
          subnet: {
            id: '${vnet.id}/subnets/AzureFirewallSubnet'
          }
          publicIPAddress: {
            id: fwip.id
          }
        }
      }
    ]
    firewallPolicy: {
      id: fwpolicy.id
    }
  }
  dependsOn: [
    aksFwRules
  ]
}

resource fwip 'Microsoft.Network/publicIPAddresses@2022-01-01' = {
  name: 'fwip'
  location: location
  sku: {
    name: 'Standard'
    tier: 'Regional'
  }
  properties: {
    publicIPAllocationMethod: 'Static'
  }
}

resource fwpolicy 'Microsoft.Network/firewallPolicies@2022-01-01' = {
  name: 'myfwpolicy'
  location: location
  properties: {
    sku: {
      tier: 'Standard'
    }
  }
}

resource aksFwRules 'Microsoft.Network/firewallPolicies/ruleCollectionGroups@2022-01-01' = {
  name: 'aksFwRules'
  parent: fwpolicy
  properties: {
    priority: 100
    ruleCollections: [
      {
        ruleCollectionType: 'FirewallPolicyFilterRuleCollection'
        name: 'aksFwRules'
        action: {
          type: 'Allow'
        }
        priority: 100
        rules: [
          {
            ruleType: 'ApplicationRule'
            name: 'aks'
            sourceAddresses: [
              '*'
            ]
            targetFqdns: [
              'mcr.microsoft.com'
              '*.data.mcr.microsoft.com'
              'management.azure.com'
              'login.microsoftonline.com'
              'packages.microsoft.com'
              'acs-mirror.azureedge.net'
            ]
            protocols: [
              {
                protocolType: 'Https'
                port: 443
              }
            ]
          }
        ]
      }
    ]
  }
}

resource aksIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2022-01-31-preview' = {
  name: 'aksidentity'
  location: location
}

resource aksIdentityRbac 'Microsoft.Authorization/roleAssignments@2020-10-01-preview' = {
  name: guid(aksIdentity.id)
  properties: {
    roleDefinitionId: '/providers/Microsoft.Authorization/roleDefinitions/4d97b98b-1d4f-4787-a291-c67834d212e7'
    principalId: aksIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource aks 'Microsoft.ContainerService/managedClusters@2022-05-02-preview' = {
  name: 'myaks'
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${aksIdentity.id}': {}
    }
  }
  properties: {
    dnsPrefix: 'myaks'
    agentPoolProfiles: [
      {
        name: 'nodes'
        count: 2
        vmSize: 'Standard_B2s'
        osType: 'Linux'
        vnetSubnetID: '${vnet.id}/subnets/nodes'
        podSubnetID: '${vnet.id}/subnets/pods'
        mode: 'System'
      }
    ]
    linuxProfile: {
      adminUsername: 'aksadmin'
      ssh: {
        publicKeys: [
          {
            keyData: 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDNN/xTE/WrpgK5nROtHupBqlHHVXQAP3c2wcvDz8PO/xLIawd8bPtrbKTmJX3TEVYe+WwQAc5K2XZrzaVGmiZeZSsHhiG3lX9kh2BbxZ9WLtLwta5gmkby4HTdk4sD3yeFFfrrdqHip5+DGl/OijUZC4ihMV6bS9P8jmugxtQKMkIeUC41HaShkXM44rnTRAvQoDr9iJZrAuuKDIZwhIv3ax8J0eu8WaRAVa5t8uZjL2Tv2QmMyK4oZtj89aVsSQyn26T3omNXfJVC/0kltM/Iu3jYXoRZz+8zAOhpTk4C6IsquM0FYsjkNBiip7/9rQCVArNMK6/Hojdl04UvVbi/QZRh4wAc9Ii49ZvD6bIxa0fc3uNl0I/EHN+BknkfzyKXuZ31roTn6xtWLcGrNN9zU+pX9Y69BvRaz2rIeYTGkQ//N7XZRV+Iv4cCEOwOrDxA61xcNDQVMLzW79Q1gQp2vD5Mybn0/LD5hb1TlAxkJfZXfdabDh/BnEEOuZFZLrgMU4c39OeQMWMV/c1gctytmLiIg4LcjhLzyzYwAShFwo+Ajkb46GWyYJD5tVnaqtf5AC6oY6C0linO6UbmpBqoWuUvM+Z6biTEP+qrUhxQ+4XVC4DwPz9Tf+YuKRvxMS5bhVxEcAFdwi1NAwfOXRMNdHRp730uslHz69gR9s3pIw=='
          }
        ]
      }
    }
    networkProfile: {
      networkPlugin: 'azure'
      outboundType: 'userDefinedRouting'
      serviceCidr: '10.0.0.0/16'
      dnsServiceIP: '10.0.0.10'
      dockerBridgeCidr: '172.17.0.1/16'
    }
    apiServerAccessProfile: {
      enablePrivateCluster: true
      privateDNSZone: 'system'
      enablePrivateClusterPublicFQDN: true
      enableVnetIntegration: true
      subnetId: '${vnet.id}/subnets/apiserver'
    }
  }
  dependsOn: [
    aksFwRules
    fw
  ]
}
