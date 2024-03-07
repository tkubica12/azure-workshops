resource "azapi_resource" "logKeyVaultToEH" {
  type      = "Microsoft.Authorization/policyDefinitions@2021-06-01"
  name      = "logKeyVaultToEH"
  parent_id = "/providers/Microsoft.Management/managementGroups/${var.root_mg_id}"
  body      = file("${path.module}/policies/logKeyVaultToEH.json")
}

resource "azapi_resource" "logFrontDoorToEH" {
  type      = "Microsoft.Authorization/policyDefinitions@2021-06-01"
  name      = "logFrontDoorToEH"
  parent_id = "/providers/Microsoft.Management/managementGroups/${var.root_mg_id}"
  body      = file("${path.module}/policies/logFrontDoorToEH.json")
}

resource "azapi_resource" "auditLogsInitiative" {
  type      = "Microsoft.Authorization/policySetDefinitions@2021-06-01"
  name      = "auditLogsInitiative"
  parent_id = "/providers/Microsoft.Management/managementGroups/${var.root_mg_id}"
  body      = <<JSON
    {
      "properties": {
        "description": "Company policy to stream logs from selected services to Event Hub",
        "displayName": "auditLogs initiative",
        "parameters": {
          "eventHubRuleId": {
            "allowedValues": null,
            "defaultValue": null,
            "metadata": {
              "description": "The Event Hub authorization rule Id for Azure Diagnostics. The authorization rule needs to be at Event Hub namespace level. e.g. /subscriptions/{subscription Id}/resourceGroups/{resource group}/providers/Microsoft.EventHub/namespaces/{Event Hub namespace}/authorizationrules/{authorization rule}",
              "displayName": "Event Hub Authorization Rule Id",
              "strongType": "Microsoft.EventHub/Namespaces/AuthorizationRules"
            },
            "type": "string"
          },
          "eventHubName": {
            "allowedValues": null,
            "defaultValue": null,
            "metadata": {
              "description": "Event Hub Name",
              "displayName": "Event Hub Name"
            },
            "type": "string"
          }
        },
        "policyDefinitions": [
          {
            "policyDefinitionReferenceId": "Key Vault to Event Hub",
            "policyDefinitionId": "${azapi_resource.logKeyVaultToEH.id}",
            "parameters": {
              "effect": {
                "value": "DeployIfNotExists"
              },
              "eventHubRuleId": {
                "value": "[parameters('eventHubRuleId')]"
              },
              "eventHubName": {
                "value": "[parameters('eventHubName')]"
              },
              "azurePolicyEvaluationDetails": {
                "value": "True"
              },
              "auditEvent": {
                "value": "True"
              }
            },
            "groupNames": []
          },
          {
            "policyDefinitionReferenceId": "Front Door to Event Hub",
            "policyDefinitionId": "${azapi_resource.logFrontDoorToEH.id}",
            "parameters": {
              "effect": {
                "value": "DeployIfNotExists"
              },
              "eventHubRuleId": {
                "value": "[parameters('eventHubRuleId')]"
              },
              "eventHubName": {
                "value": "[parameters('eventHubName')]"
              },
              "FrontDoorAccessLog": {
                "value": "True"
              },
              "FrontDoorHealthProbeLog": {
                "value": "False"
              },
              "FrontDoorWebApplicationFirewallLog": {
                "value": "True"
              }
            },
            "groupNames": []
          }
        ]
      }
    }
  JSON
}

