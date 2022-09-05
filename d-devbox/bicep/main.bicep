var location = resourceGroup().location

resource devcenter 'Microsoft.DevCenter/devcenters@2022-08-01-preview' = {
  name: 'mydevcenter'
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${devbox_identity.id}': {}
    }
  }
}

// Dev Box Managed Identity
resource devbox_identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2022-01-31-preview' = {
  name: 'devcenter'
  location: location
}

// Network
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
        name: 'devbox'
        properties: {
          addressPrefix: '10.88.0.0/24'
        }
      }
    ]
  }
}

// Dev Center Network connection
resource devcenter_network 'Microsoft.DevCenter/networkConnections@2022-08-01-preview' = {
  name: 'myvnetconnection'
  location: location
  properties: {
    domainJoinType: 'AzureADJoin'
    subnetId: '${vnet.id}/subnets/devbox'
  }
}

// Projects
resource project1 'Microsoft.DevCenter/projects@2022-08-01-preview' = {
  name: 'myproject1'
  location: location
  properties: {
    devCenterId: devcenter.id
  }
}

// Dev boxes
resource devbox_coder 'Microsoft.DevCenter/devcenters/devboxdefinitions@2022-08-01-preview' = {
  parent: devcenter
  name: 'mydevbox_coder'
  location: location
  properties: {
    sku: {
      name: 'general_a_4c16gb_v1'
    }
    imageReference: {
      id: '${devcenter.id}/galleries/default/images/microsoftwindowsdesktop_windows-ent-cpc_win11-21h2-ent-cpc-os'
    }
    osStorageType: 'ssd_256gb'
  }
}

resource devbox_dba 'Microsoft.DevCenter/devcenters/devboxdefinitions@2022-08-01-preview' = {
  parent: devcenter
  name: 'mydevbox_dba'
  location: location
  properties: {
    sku: {
      name: 'general_a_4c16gb_v1'
    }
    imageReference: {
      id: '${devcenter.id}/galleries/default/images/microsoftwindowsdesktop_windows-ent-cpc_win11-21h2-ent-cpc-os'
    }
    osStorageType: 'ssd_256gb'
  }
}

// Dev Box pools
resource devboxpool_coder 'Microsoft.DevCenter/projects/pools@2022-08-01-preview' = {
  parent: project1
  name: 'mydevboxpool_coder'
  location: location
  properties: {
    devBoxDefinitionName: devbox_coder.name
    networkConnectionName: devcenter_network.name
    licenseType: 'Windows_Client'
    localAdministrator: 'Enabled'
  }
}

resource devboxpool_dba 'Microsoft.DevCenter/projects/pools@2022-08-01-preview' = {
  parent: project1
  name: 'mydevboxpool_dba'
  location: location
  properties: {
    devBoxDefinitionName: devbox_coder.name
    networkConnectionName: devcenter_network.name
    licenseType: 'Windows_Client'
    localAdministrator: 'Enabled'
  }
}

// Give developers access to the dev projects
resource rbac_devbox_current_user 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid('current_user')
  properties: {
    principalId: 'd3b7888f-c26e-4961-a976-ff9d5b31dfd3'
    roleDefinitionId: '/providers/Microsoft.Authorization/roleDefinitions/45d50f46-0b7' // DevCenter Dev Box User
  }
}
