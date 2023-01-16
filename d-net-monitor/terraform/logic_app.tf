resource "azurerm_logic_app_workflow" "main" {
  name                = random_string.main.result
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_logic_app_trigger_http_request" "main" {
  name         = "alert"
  logic_app_id = azurerm_logic_app_workflow.main.id

  schema = <<EOF
{
    "properties": {
        "data": {
            "properties": {
                "context": {
                    "properties": {
                        "condition": {
                            "properties": {
                                "allOf": {
                                    "items": {
                                        "properties": {
                                            "dimensions": {
                                                "items": {
                                                    "properties": {
                                                        "name": {
                                                            "type": "string"
                                                        },
                                                        "value": {
                                                            "type": "string"
                                                        }
                                                    },
                                                    "required": [
                                                        "name",
                                                        "value"
                                                    ],
                                                    "type": "object"
                                                },
                                                "type": "array"
                                            },
                                            "metricName": {
                                                "type": "string"
                                            },
                                            "metricValue": {
                                                "type": "integer"
                                            },
                                            "operator": {
                                                "type": "string"
                                            },
                                            "threshold": {
                                                "type": "string"
                                            },
                                            "timeAggregation": {
                                                "type": "string"
                                            }
                                        },
                                        "required": [
                                            "metricName",
                                            "dimensions",
                                            "operator",
                                            "threshold",
                                            "timeAggregation",
                                            "metricValue"
                                        ],
                                        "type": "object"
                                    },
                                    "type": "array"
                                },
                                "windowSize": {
                                    "type": "string"
                                }
                            },
                            "type": "object"
                        },
                        "conditionType": {
                            "type": "string"
                        },
                        "description": {
                            "type": "string"
                        },
                        "id": {
                            "type": "string"
                        },
                        "name": {
                            "type": "string"
                        },
                        "portalLink": {
                            "type": "string"
                        },
                        "resourceGroupName": {
                            "type": "string"
                        },
                        "resourceId": {
                            "type": "string"
                        },
                        "resourceName": {
                            "type": "string"
                        },
                        "resourceType": {
                            "type": "string"
                        },
                        "subscriptionId": {
                            "type": "string"
                        },
                        "timestamp": {
                            "type": "string"
                        }
                    },
                    "type": "object"
                },
                "properties": {
                    "properties": {},
                    "type": "object"
                },
                "status": {
                    "type": "string"
                },
                "version": {
                    "type": "string"
                }
            },
            "type": "object"
        },
        "schemaId": {
            "type": "string"
        }
    },
    "type": "object"
}
EOF
}

resource "azurerm_logic_app_action_custom" "Initialize_variable_teamId" {
  name         = "Initialize_variable_teamId"
  logic_app_id = azurerm_logic_app_workflow.main.id

  body = <<EOF
{
    "runAfter": {},
    "type": "InitializeVariable",
    "inputs": {
        "variables": [
            {
                "name": "teamId",
                "type": "string"
            }
        ]
    }
}
EOF
}

resource "azurerm_logic_app_action_custom" "Initialize_variable_channelId" {
  name         = "Initialize_variable_channelId"
  logic_app_id = azurerm_logic_app_workflow.main.id

  depends_on = [
    azurerm_logic_app_action_custom.Initialize_variable_teamId
  ]

  body = <<EOF
{
    "runAfter": {
        "Initialize_variable_teamId": [
            "Succeeded"
        ]
    },
    "type": "InitializeVariable",
    "inputs": {
        "variables": [
            {
                "name": "channelId",
                "type": "string"
            }
        ]
    }
}
EOF
}

resource "azurerm_logic_app_action_custom" "List_teams" {
  name         = "List_teams"
  logic_app_id = azurerm_logic_app_workflow.main.id

  depends_on = [
    azurerm_logic_app_action_custom.Initialize_variable_channelId
  ]

  body = <<EOF
{
    "runAfter": {
        "Initialize_variable_channelId": [
            "Succeeded"
        ]
    },
    "type": "ApiConnection",
    "inputs": {
        "host": {
            "connection": {
                "name": "@parameters('$connections')['teams']['connectionId']"
            }
        },
        "method": "get",
        "path": "/beta/me/joinedTeams"
    }
}
EOF
}

resource "azurerm_logic_app_action_custom" "For_each_team_name" {
  name         = "For_each_team_name"
  logic_app_id = azurerm_logic_app_workflow.main.id

  depends_on = [
    azurerm_logic_app_action_custom.List_teams
  ]

  body = <<EOF
{
    "foreach": "@body('List_teams')?['value']",
    "actions": {
        "Is_target_team_name_presented_in_a_list": {
            "actions": {
                "Set_variable_teamId_to_existing_team": {
                    "runAfter": {},
                    "type": "SetVariable",
                    "inputs": {
                        "name": "teamId",
                        "value": "@items('For_each_team_name')?['id']"
                    }
                }
            },
            "runAfter": {},
            "expression": {
                "and": [
                    {
                        "equals": [
                            "@items('For_each_team_name')?['displayName']",
                            "d-net-monitor"
                        ]
                    }
                ]
            },
            "type": "If"
        }
    },
    "runAfter": {
        "List_teams": [
            "Succeeded"
        ]
    },
    "type": "Foreach"
}
EOF
}

resource "azurerm_logic_app_action_custom" "Create_team_if_not_exists" {
  name         = "Create_team_if_not_exists"
  logic_app_id = azurerm_logic_app_workflow.main.id

  depends_on = [
    azurerm_logic_app_action_custom.For_each_team_name
  ]

  body = <<EOF
{
    "actions": {},
    "runAfter": {
        "For_each_team_name": [
            "Succeeded"
        ]
    },
    "else": {
        "actions": {
            "Create_a_team": {
                "runAfter": {},
                "type": "ApiConnection",
                "inputs": {
                    "body": {
                        "description": "d-net-monitor demo",
                        "displayName": "d-net-monitor",
                        "visibility": "Public"
                    },
                    "host": {
                        "connection": {
                            "name": "@parameters('$connections')['teams']['connectionId']"
                        }
                    },
                    "method": "post",
                    "path": "/beta/teams"
                }
            },
            "Set_variable_teamId_to_new_team": {
                "runAfter": {
                    "Create_a_team": [
                        "Succeeded"
                    ]
                },
                "type": "SetVariable",
                "inputs": {
                    "name": "teamId",
                    "value": "@body('Create_a_team')?['newTeamId']"
                }
            }
        }
    },
    "expression": {
        "and": [
            {
                "not": {
                    "equals": [
                        "@variables('teamId')",
                        ""
                    ]
                }
            }
        ]
    },
    "type": "If"
}
EOF
}

resource "azurerm_logic_app_action_custom" "Add_a_member_to_a_team" {
  name         = "Add_a_member_to_a_team"
  logic_app_id = azurerm_logic_app_workflow.main.id

  depends_on = [
    azurerm_logic_app_action_custom.Create_team_if_not_exists
  ]

  body = <<EOF
{
    "runAfter": {
        "Create_team_if_not_exists": [
            "Succeeded"
        ]
    },
    "type": "ApiConnection",
    "inputs": {
        "body": {
            "owner": true,
            "userId": "admin@tkubica.biz"
        },
        "host": {
            "connection": {
                "name": "@parameters('$connections')['teams']['connectionId']"
            }
        },
        "method": "post",
        "path": "/beta/teams/@{encodeURIComponent(variables('teamId'))}/members"
    }
}
EOF
}

resource "azurerm_logic_app_action_custom" "List_channels" {
  name         = "List_channels"
  logic_app_id = azurerm_logic_app_workflow.main.id

  depends_on = [
    azurerm_logic_app_action_custom.Add_a_member_to_a_team
  ]

  body = <<EOF
{
    "runAfter": {
        "Add_a_member_to_a_team": [
            "Succeeded"
        ]
    },
    "type": "ApiConnection",
    "inputs": {
        "host": {
            "connection": {
                "name": "@parameters('$connections')['teams']['connectionId']"
            }
        },
        "method": "get",
        "path": "/beta/groups/@{encodeURIComponent(variables('teamId'))}/channels"
    }
}
EOF
}

resource "azurerm_logic_app_action_custom" "For_each_channel_name" {
  name         = "For_each_channel_name"
  logic_app_id = azurerm_logic_app_workflow.main.id

  depends_on = [
    azurerm_logic_app_action_custom.List_channels
  ]

  body = <<EOF
{
    "foreach": "@body('List_channels')?['value']",
    "actions": {
        "Is_target_channel_name_presented_in_a_list": {
            "actions": {
                "Set_variable_channelId_to_existing_channel": {
                    "runAfter": {},
                    "type": "SetVariable",
                    "inputs": {
                        "name": "channelId",
                        "value": "@items('For_each_channel_name')?['id']"
                    }
                }
            },
            "runAfter": {},
            "expression": {
                "and": [
                    {
                        "equals": [
                            "@items('For_each_channel_name')?['displayName']",
                            "MyDemoErrors"
                        ]
                    }
                ]
            },
            "type": "If"
        }
    },
    "runAfter": {
        "List_channels": [
            "Succeeded"
        ]
    },
    "type": "Foreach"
}
EOF
}

resource "azurerm_logic_app_action_custom" "Create_channel_if_not_exists" {
  name         = "Create_channel_if_not_exists"
  logic_app_id = azurerm_logic_app_workflow.main.id

  depends_on = [
    azurerm_logic_app_action_custom.For_each_channel_name
  ]

  body = <<EOF
{
    "actions": {},
    "runAfter": {
        "For_each_channel_name": [
            "Succeeded"
        ]
    },
    "else": {
        "actions": {
            "Create_a_channel": {
                "runAfter": {},
                "type": "ApiConnection",
                "inputs": {
                    "body": {
                        "displayName": "MyDemoErrors"
                    },
                    "host": {
                        "connection": {
                            "name": "@parameters('$connections')['teams']['connectionId']"
                        }
                    },
                    "method": "post",
                    "path": "/beta/groups/@{encodeURIComponent(variables('teamId'))}/channels"
                }
            },
            "Set_variable_channelId_to_new_channel": {
                "runAfter": {
                    "Create_a_channel": [
                        "Succeeded"
                    ]
                },
                "type": "SetVariable",
                "inputs": {
                    "name": "channelId",
                    "value": "@body('Create_a_channel')?['id']"
                }
            }
        }
    },
    "expression": {
        "and": [
            {
                "not": {
                    "equals": [
                        "@variables('channelId')",
                        ""
                    ]
                }
            }
        ]
    },
    "type": "If"
}
EOF
}

resource "azurerm_logic_app_action_custom" "Post_message_in_a_chat_or_channel" {
  name         = "Post_message_in_a_chat_or_channel"
  logic_app_id = azurerm_logic_app_workflow.main.id

  depends_on = [
    azurerm_logic_app_action_custom.Create_channel_if_not_exists
  ]

  body = <<EOF
{
    "runAfter": {
        "Create_channel_if_not_exists": [
            "Succeeded"
        ]
    },
    "type": "ApiConnection",
    "inputs": {
        "body": {
            "messageBody": "<p>New message:<br>\n<br>\n@{triggerBody()}</p>",
            "recipient": {
                "channelId": "@variables('channelId')",
                "groupId": "@variables('teamId')"
            }
        },
        "host": {
            "connection": {
                "name": "@parameters('$connections')['teams']['connectionId']"
            }
        },
        "method": "post",
        "path": "/beta/teams/conversation/message/poster/@{encodeURIComponent('User')}/location/@{encodeURIComponent('Channel')}"
    }
}
EOF
}










# data "azurerm_managed_api" "example" {
#   name     = "teams"
#   location = azurerm_resource_group.main.location
# }

# resource "azurerm_resource_group_template_deployment" "logicapp" {
#   name                = random_string.main.result
#   resource_group_name = azurerm_resource_group.main.name

#   template_content = <<EOF
# {
#     "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
#     "contentVersion": "1.0.0.0",
#     "parameters": {},
#     "variables": {},
#     "resources": [
#         {
#             "type": "Microsoft.Logic/workflows",
#             "apiVersion": "2017-07-01",
#             "name": "${random_string.main.result}",
#             "location": "westeurope",
#             "properties": {
#                 "state": "Enabled",
#                 "definition": {
#                     "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
#                     "contentVersion": "1.0.0.0",
#                     "parameters": {
#                         "$connections": {
#                             "defaultValue": {},
#                             "type": "Object"
#                         }
#                     },
#                     "triggers": {
#                         "manual": {
#                             "type": "Request",
#                             "kind": "Http",
#                             "inputs": {
#                                 "schema": {
#                                     "properties": {
#                                         "data": {
#                                             "properties": {
#                                                 "context": {
#                                                     "properties": {
#                                                         "condition": {
#                                                             "properties": {
#                                                                 "allOf": {
#                                                                     "items": {
#                                                                         "properties": {
#                                                                             "dimensions": {
#                                                                                 "items": {
#                                                                                     "properties": {
#                                                                                         "name": {
#                                                                                             "type": "string"
#                                                                                         },
#                                                                                         "value": {
#                                                                                             "type": "string"
#                                                                                         }
#                                                                                     },
#                                                                                     "required": [
#                                                                                         "name",
#                                                                                         "value"
#                                                                                     ],
#                                                                                     "type": "object"
#                                                                                 },
#                                                                                 "type": "array"
#                                                                             },
#                                                                             "metricName": {
#                                                                                 "type": "string"
#                                                                             },
#                                                                             "metricValue": {
#                                                                                 "type": "integer"
#                                                                             },
#                                                                             "operator": {
#                                                                                 "type": "string"
#                                                                             },
#                                                                             "threshold": {
#                                                                                 "type": "string"
#                                                                             },
#                                                                             "timeAggregation": {
#                                                                                 "type": "string"
#                                                                             }
#                                                                         },
#                                                                         "required": [
#                                                                             "metricName",
#                                                                             "dimensions",
#                                                                             "operator",
#                                                                             "threshold",
#                                                                             "timeAggregation",
#                                                                             "metricValue"
#                                                                         ],
#                                                                         "type": "object"
#                                                                     },
#                                                                     "type": "array"
#                                                                 },
#                                                                 "windowSize": {
#                                                                     "type": "string"
#                                                                 }
#                                                             },
#                                                             "type": "object"
#                                                         },
#                                                         "conditionType": {
#                                                             "type": "string"
#                                                         },
#                                                         "description": {
#                                                             "type": "string"
#                                                         },
#                                                         "id": {
#                                                             "type": "string"
#                                                         },
#                                                         "name": {
#                                                             "type": "string"
#                                                         },
#                                                         "portalLink": {
#                                                             "type": "string"
#                                                         },
#                                                         "resourceGroupName": {
#                                                             "type": "string"
#                                                         },
#                                                         "resourceId": {
#                                                             "type": "string"
#                                                         },
#                                                         "resourceName": {
#                                                             "type": "string"
#                                                         },
#                                                         "resourceType": {
#                                                             "type": "string"
#                                                         },
#                                                         "subscriptionId": {
#                                                             "type": "string"
#                                                         },
#                                                         "timestamp": {
#                                                             "type": "string"
#                                                         }
#                                                     },
#                                                     "type": "object"
#                                                 },
#                                                 "properties": {
#                                                     "properties": {},
#                                                     "type": "object"
#                                                 },
#                                                 "status": {
#                                                     "type": "string"
#                                                 },
#                                                 "version": {
#                                                     "type": "string"
#                                                 }
#                                             },
#                                             "type": "object"
#                                         },
#                                         "schemaId": {
#                                             "type": "string"
#                                         }
#                                     },
#                                     "type": "object"
#                                 }
#                             }
#                         }
#                     },
#                     "actions": {
#                         "Add_a_member_to_a_team": {
#                             "runAfter": {
#                                 "Create_team_if_not_exists": [
#                                     "Succeeded"
#                                 ]
#                             },
#                             "type": "ApiConnection",
#                             "inputs": {
#                                 "body": {
#                                     "owner": true,
#                                     "userId": "admin@tkubica.biz"
#                                 },
#                                 "host": {
#                                     "connection": {
#                                         "name": "@parameters('$connections')['teams']['connectionId']"
#                                     }
#                                 },
#                                 "method": "post",
#                                 "path": "/beta/teams/@{encodeURIComponent(variables('teamId'))}/members"
#                             }
#                         },
#                         "Create_channel_if_not_exists": {
#                             "actions": {},
#                             "runAfter": {
#                                 "For_each_channel_name": [
#                                     "Succeeded"
#                                 ]
#                             },
#                             "else": {
#                                 "actions": {
#                                     "Create_a_channel": {
#                                         "runAfter": {},
#                                         "type": "ApiConnection",
#                                         "inputs": {
#                                             "body": {
#                                                 "displayName": "MyDemoErrors"
#                                             },
#                                             "host": {
#                                                 "connection": {
#                                                     "name": "@parameters('$connections')['teams']['connectionId']"
#                                                 }
#                                             },
#                                             "method": "post",
#                                             "path": "/beta/groups/@{encodeURIComponent(variables('teamId'))}/channels"
#                                         }
#                                     },
#                                     "Set_variable_channelId_to_new_channel": {
#                                         "runAfter": {
#                                             "Create_a_channel": [
#                                                 "Succeeded"
#                                             ]
#                                         },
#                                         "type": "SetVariable",
#                                         "inputs": {
#                                             "name": "channelId",
#                                             "value": "@body('Create_a_channel')?['id']"
#                                         }
#                                     }
#                                 }
#                             },
#                             "expression": {
#                                 "and": [
#                                     {
#                                         "not": {
#                                             "equals": [
#                                                 "@variables('channelId')",
#                                                 ""
#                                             ]
#                                         }
#                                     }
#                                 ]
#                             },
#                             "type": "If"
#                         },
#                         "Create_team_if_not_exists": {
#                             "actions": {},
#                             "runAfter": {
#                                 "For_each_team_name": [
#                                     "Succeeded"
#                                 ]
#                             },
#                             "else": {
#                                 "actions": {
#                                     "Create_a_team": {
#                                         "runAfter": {},
#                                         "type": "ApiConnection",
#                                         "inputs": {
#                                             "body": {
#                                                 "description": "d-net-monitor demo",
#                                                 "displayName": "d-net-monitor",
#                                                 "visibility": "Public"
#                                             },
#                                             "host": {
#                                                 "connection": {
#                                                     "name": "@parameters('$connections')['teams']['connectionId']"
#                                                 }
#                                             },
#                                             "method": "post",
#                                             "path": "/beta/teams"
#                                         }
#                                     },
#                                     "Set_variable_teamId_to_new_team": {
#                                         "runAfter": {
#                                             "Create_a_team": [
#                                                 "Succeeded"
#                                             ]
#                                         },
#                                         "type": "SetVariable",
#                                         "inputs": {
#                                             "name": "teamId",
#                                             "value": "@body('Create_a_team')?['newTeamId']"
#                                         }
#                                     }
#                                 }
#                             },
#                             "expression": {
#                                 "and": [
#                                     {
#                                         "not": {
#                                             "equals": [
#                                                 "@variables('teamId')",
#                                                 ""
#                                             ]
#                                         }
#                                     }
#                                 ]
#                             },
#                             "type": "If"
#                         },
#                         "For_each_channel_name": {
#                             "foreach": "@body('List_channels')?['value']",
#                             "actions": {
#                                 "Is_target_channel_name_presented_in_a_list": {
#                                     "actions": {
#                                         "Set_variable_channelId_to_existing_channel": {
#                                             "runAfter": {},
#                                             "type": "SetVariable",
#                                             "inputs": {
#                                                 "name": "channelId",
#                                                 "value": "@items('For_each_channel_name')?['id']"
#                                             }
#                                         }
#                                     },
#                                     "runAfter": {},
#                                     "expression": {
#                                         "and": [
#                                             {
#                                                 "equals": [
#                                                     "@items('For_each_channel_name')?['displayName']",
#                                                     "MyDemoErrors"
#                                                 ]
#                                             }
#                                         ]
#                                     },
#                                     "type": "If"
#                                 }
#                             },
#                             "runAfter": {
#                                 "List_channels": [
#                                     "Succeeded"
#                                 ]
#                             },
#                             "type": "Foreach"
#                         },
#                         "For_each_team_name": {
#                             "foreach": "@body('List_teams')?['value']",
#                             "actions": {
#                                 "Is_target_team_name_presented_in_a_list": {
#                                     "actions": {
#                                         "Set_variable_teamId_to_existing_team": {
#                                             "runAfter": {},
#                                             "type": "SetVariable",
#                                             "inputs": {
#                                                 "name": "teamId",
#                                                 "value": "@items('For_each_team_name')?['id']"
#                                             }
#                                         }
#                                     },
#                                     "runAfter": {},
#                                     "expression": {
#                                         "and": [
#                                             {
#                                                 "equals": [
#                                                     "@items('For_each_team_name')?['displayName']",
#                                                     "d-net-monitor"
#                                                 ]
#                                             }
#                                         ]
#                                     },
#                                     "type": "If"
#                                 }
#                             },
#                             "runAfter": {
#                                 "List_teams": [
#                                     "Succeeded"
#                                 ]
#                             },
#                             "type": "Foreach"
#                         },
#                         "Initialize_variable_channelId": {
#                             "runAfter": {
#                                 "Initialize_variable_teamId": [
#                                     "Succeeded"
#                                 ]
#                             },
#                             "type": "InitializeVariable",
#                             "inputs": {
#                                 "variables": [
#                                     {
#                                         "name": "channelId",
#                                         "type": "string"
#                                     }
#                                 ]
#                             }
#                         },
#                         "Initialize_variable_teamId": {
#                             "runAfter": {},
#                             "type": "InitializeVariable",
#                             "inputs": {
#                                 "variables": [
#                                     {
#                                         "name": "teamId",
#                                         "type": "string"
#                                     }
#                                 ]
#                             }
#                         },
#                         "List_channels": {
#                             "runAfter": {
#                                 "Add_a_member_to_a_team": [
#                                     "Succeeded"
#                                 ]
#                             },
#                             "type": "ApiConnection",
#                             "inputs": {
#                                 "host": {
#                                     "connection": {
#                                         "name": "@parameters('$connections')['teams']['connectionId']"
#                                     }
#                                 },
#                                 "method": "get",
#                                 "path": "/beta/groups/@{encodeURIComponent(variables('teamId'))}/channels"
#                             }
#                         },
#                         "List_teams": {
#                             "runAfter": {
#                                 "Initialize_variable_channelId": [
#                                     "Succeeded"
#                                 ]
#                             },
#                             "type": "ApiConnection",
#                             "inputs": {
#                                 "host": {
#                                     "connection": {
#                                         "name": "@parameters('$connections')['teams']['connectionId']"
#                                     }
#                                 },
#                                 "method": "get",
#                                 "path": "/beta/me/joinedTeams"
#                             }
#                         },
#                         "Post_message_in_a_chat_or_channel": {
#                             "runAfter": {
#                                 "Create_channel_if_not_exists": [
#                                     "Succeeded"
#                                 ]
#                             },
#                             "type": "ApiConnection",
#                             "inputs": {
#                                 "body": {
#                                     "messageBody": "<p>New message:<br>\n<br>\n@{triggerBody()}</p>",
#                                     "recipient": {
#                                         "channelId": "@variables('channelId')",
#                                         "groupId": "@variables('teamId')"
#                                     }
#                                 },
#                                 "host": {
#                                     "connection": {
#                                         "name": "@parameters('$connections')['teams']['connectionId']"
#                                     }
#                                 },
#                                 "method": "post",
#                                 "path": "/beta/teams/conversation/message/poster/@{encodeURIComponent('User')}/location/@{encodeURIComponent('Channel')}"
#                             }
#                         }
#                     },
#                     "outputs": {}
#                 },
#                 "parameters": {
#                     "$connections": {
#                         "value": {
#                             "teams": {
#                                 "connectionId": "/subscriptions/d3b7888f-c26e-4961-a976-ff9d5b31dfd3/resourceGroups/d-net-monitor/providers/Microsoft.Web/connections/teams",
#                                 "connectionName": "teams",
#                                 "id": "/subscriptions/d3b7888f-c26e-4961-a976-ff9d5b31dfd3/providers/Microsoft.Web/locations/westeurope/managedApis/teams"
#                             }
#                         }
#                     }
#                 }
#             }
#         }
#     ]
# }
# EOF
# }
