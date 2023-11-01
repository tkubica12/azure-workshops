resource "azapi_resource" "policySubRoleDeny" {
  type      = "Microsoft.Authorization/policyDefinitions@2021-06-01"
  name      = "policySubRoleDeny"
  parent_id = "/subscriptions/${var.subscription_id}"
  body      = file("${path.module}/policies/policySubRoleDeny.json")
}

resource "azapi_resource" "assignmentSubRoleDeny" {
  type      = "Microsoft.Authorization/policyAssignments@2022-06-01"
  name      = "assignmentSubRoleDeny"
  location  = var.location
  parent_id = "/subscriptions/${var.subscription_id}"
  body = jsonencode({
    properties = {
      description     = "assignmentSubRoleDeny"
      displayName     = "assignmentSubRoleDeny"
      enforcementMode = "Default"
      nonComplianceMessages = [
        {
          message = "Assignment of role on this scope is forbidden by company policy, please try different scope or contact your administrator."
        }
      ]
      notScopes = [
        "/subscriptions/${var.subscription_id}/resourceGroups"
      ]
      parameters         = {}
      policyDefinitionId = azapi_resource.policySubRoleDeny.id
    }
  })
}
