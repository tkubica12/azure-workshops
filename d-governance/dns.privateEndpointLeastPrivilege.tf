// Resource Group for Private DNS zones
resource "azapi_resource" "dns_rg" {
  type      = "Microsoft.Resources/resourceGroups@2022-09-01"
  name      = "dns-rg"
  location  = var.location
  parent_id = "/subscriptions/${var.hub_subscription_id}"

  body = jsonencode({
    properties = {}
  })
}

// Private DNS zone for blob storage
resource "azapi_resource" "dns_blob" {
  type      = "Microsoft.Network/privateDnsZones@2020-06-01"
  name      = "privatelink.blob.core.windows.net"
  location  = "global"
  parent_id = azapi_resource.dns_rg.id

  body = jsonencode({
    properties = {}
  })
}

// Resource Group in user subscription
resource "azapi_resource" "user_rg" {
  type      = "Microsoft.Resources/resourceGroups@2022-09-01"
  name      = "user-rg"
  location  = var.location
  parent_id = "/subscriptions/${var.subscription_id}"

  body = jsonencode({
    properties = {}
  })
}

// RBAC - user to be contributor in user RG
resource "random_uuid" "user_role_assignment" {}

resource "azapi_resource" "user_role_assignment" {
  type      = "Microsoft.Authorization/roleAssignments@2020-04-01-preview"
  name      = random_uuid.user_role_assignment.result
  parent_id = azapi_resource.user_rg.id

  body = jsonencode({
    properties = {
      principalId      = var.user_object_id
      roleDefinitionId = "/providers/Microsoft.Authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c"
    }
  })
}

// Create custom RBAC role for joining private DNS zones with Private Endpoints
resource "random_uuid" "dns_join_role" {}

resource "azapi_resource" "dns_join_role" {
  type      = "Microsoft.Authorization/roleDefinitions@2022-04-01"
  name      = random_uuid.dns_join_role.result
  parent_id = "/providers/Microsoft.Management/managementGroups/${var.root_mg_id}"

  body = jsonencode({
    properties = {
      assignableScopes = [
        "/providers/Microsoft.Management/managementGroups/${var.root_mg_id}"
      ]
      description = "Custom RBAC role for joining private DNS zones with Private Endpoints"
      permissions = [
        {
          actions = [
            "Microsoft.Network/privateDnsZones/read",
            "Microsoft.Resources/subscriptions/resourceGroups/read",
            "Microsoft.Network/privateDnsZones/join/action"
          ]
          dataActions    = []
          notActions     = []
          notDataActions = []
        }
      ]
      roleName = "dnsJoin"
    }
  })
}

// RBAC - user to be contributor in user RG
resource "random_uuid" "dns_role_assignment" {}

resource "azapi_resource" "dns_role_assignment" {
  type      = "Microsoft.Authorization/roleAssignments@2020-04-01-preview"
  name      = random_uuid.dns_role_assignment.result
  parent_id = azapi_resource.dns_rg.id

  body = jsonencode({
    properties = {
      principalId      = var.user_object_id
      roleDefinitionId = azapi_resource.dns_join_role.id
    }
  })
}

// Create storage account
resource "random_string" "storage_account_name" {
  length  = 16
  special = false
  numeric = false
  upper   = false
  lower   = true
}

resource "azapi_resource" "storage_account" {
  type      = "Microsoft.Storage/storageAccounts@2022-09-01"
  name      = random_string.storage_account_name.result
  location  = var.location
  parent_id = azapi_resource.user_rg.id

  body = jsonencode({
    kind = "StorageV2"
    sku = {
      name = "Standard_LRS"
    }
    properties = {}
  })
}

// User VNET
resource "azapi_resource" "user_vnet" {
  type      = "Microsoft.Network/virtualNetworks@2023-04-01"
  name      = "user-vnet"
  location  = var.location
  parent_id = azapi_resource.user_rg.id

  body = jsonencode({
    properties = {
      addressSpace = {
        addressPrefixes = [
          "10.0.0.0/16"
        ]
      }
      subnets = [
        {
          name = "default"
          properties = {
            addressPrefix = "10.0.0.0/24"
          }
        }
      ]
    }
  })
}

// Azure Policy definition to deny creation of privatelink DNS zones
resource "azapi_resource" "policyPrivateLinkDnsDeny" {
  type      = "Microsoft.Authorization/policyDefinitions@2021-06-01"
  name      = "policyPrivateLinkDnsDeny"
  parent_id = "/subscriptions/${var.subscription_id}"
  body      = file("${path.module}/policies/policyPrivateLinkDnsDeny.json")
}

// Assign policy
resource "azapi_resource" "assignmentPrivateLinkDnsDeny" {
  type      = "Microsoft.Authorization/policyAssignments@2022-06-01"
  name      = "assignmentPrivateLinkDnsDeny"
  location  = var.location
  parent_id = "/subscriptions/${var.subscription_id}"

  body = jsonencode({
    properties = {
      description     = "assignmentPrivateLinkDnsDeny"
      displayName     = "assignmentPrivateLinkDnsDeny"
      enforcementMode = "Default"
      nonComplianceMessages = [
        {
          message = "Creation of privatelink DNS zones in user subscription is not allowed by company policy. Please use our central private DNS zones that are integrated with hybrid DNS system."
        }
      ]
      notScopes          = []
      parameters         = {}
      policyDefinitionId = azapi_resource.policyPrivateLinkDnsDeny.id
    }
  })
}
