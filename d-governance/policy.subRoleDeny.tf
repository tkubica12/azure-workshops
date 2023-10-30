resource "azapi_resource" "policySubRoleDeny" {
  type      = "Microsoft.Authorization/policyDefinitions@2021-06-01"
  name      = "policySubRoleDeny"
  parent_id = "/subscriptions/${var.subscription_id}"
  body = jsonencode({
    properties = {
      "mode" : "All",
      "policyRule" : {
        "if" : {
          "allOf" : [
            {
              "field" : "type",
              "equals" : "Microsoft.Authorization/roleAssignments"
            },
            {
              "field" : "Microsoft.Authorization/roleAssignments/roleDefinitionId",
              "contains" : "8e3af657-a8ff-443c-a75c-2fe8c4bcb635" # Owner
            }
          ]
        },
        "then" : {
          "effect" : "[parameters('effect')]"
        }
      },
      "parameters" : {
        "effect" : {
          "type" : "String",
          "metadata" : {
            "displayName" : "Effect",
            "description" : "Effect of this Azure Policy - Audit, Deny or Disabled"
          },
          "allowedValues" : [
            "Audit",
            "Deny",
            "Disabled"
          ],
          "defaultValue" : "Deny"
        }
      }
    }
  })
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
      #   resourceSelectors = [
      #     {
      #       name = "subScope"
      #       selectors = [
      #         {
      #           kind = "resourceType"
      #           in = [
      #             "string"
      #           ]
      #           notIn = [
      #             "string"
      #           ]
      #         }
      #       ]
      #     }
      #   ]
    }
  })
}
