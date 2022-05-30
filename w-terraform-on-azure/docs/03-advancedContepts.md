# Lab 3 - More advanced concepts: versioning, conditions, structure inputs and abstractions, cycles


## Conditionals
As first tak we will want make our Azure SQL module more universal by adding configuration of auditing to Azure Monitor (Log Analytics workspace is being created in root module already), but conditionaly. We want to configure this for our produciton deployments, but not for dev environments to save costs. We need to make sure module can be parametrized to deploy auditing only when asked for.

Here are resources to be placed in module (do not forget to also decalre logWorkspaceId variable):

```
resource "azurerm_mssql_database_extended_auditing_policy" "module" {
  database_id            = azurerm_mssql_database.test.id
  log_monitoring_enabled = true
}

resource "azurerm_mssql_server_extended_auditing_policy" "module" {
  server_id              = azurerm_mssql_database.test.id
  log_monitoring_enabled = true
}

resource "azurerm_monitor_diagnostic_setting" "module" {
  name                       = "${azurerm_mssql_server.module.name}-logs"
  target_resource_id         = "${azurerm_mssql_server.module.id}/databases/master"
  log_analytics_workspace_id = var.logWorkspaceId

  log {
    category = "SQLSecurityAuditEvents"
    enabled  = true

    retention_policy {
      enabled = false
    }
  }

  lifecycle {
    ignore_changes = [log, metric]
  }
}
```

Now let's declare boolean variable called enableAudit (should default to false) and deploy resources only when this is set to true. You can use loops for this - count specifies number of iterations and we will use 1 when enableAudit is true and 0 when enableAudit is false.

```
 count                      = var.enableAudit ? 1 : 0
```

No without any changes to your root module use ```terraform plan``` and make sure there are no errors or resources being planned. Then configure root module to deploy with enableAudit se to true and logWorkspaceId set. See additional resources in ```terraform plan``` and than apply.

## Loops
Often you need to create the same resource mutliple times, call module multiple times or repeat one structure inside resource. Terraform supports loops on all mentioned levels. It is often preferable to use for each with map so keys are fixed and predictable. Using simple for loop with index number might have negative side effects eg. if you insert item in array (than it might renumber therefore recreate all resources which might cause downtime - eg. when touching existing firewall rules).

We will want to create multiple databases and rather than having separate module calls create input abstraction map and loop over it. 

This is required structure (put it into your root module):

```locals {
  databases = {
    tomdb1 = {
      skuName = "S0"
      dbName = "db1"
    }
    tomdb2 = {
      skuName = "S0"
      dbName = "db2"
    }
    tomdb3 = {
      skuName = "S0"
      dbName = "db3"
    }
  }
}
```

Use for each to loop over this map with your azure sql module [https://www.terraform.io/language/meta-arguments/for_each](https://www.terraform.io/language/meta-arguments/for_each)

Note your output from root module will no longer work so change it to this to return list of outputs from all azuresql module instances:
```
output "sqlNames" {
  value = values(module.sql)[*].name
}
```

## Move input data structure to separate YAML file
Terraform can load files: [https://www.terraform.io/language/functions/file](https://www.terraform.io/language/functions/file)
Terraform can decode YAML: [https://www.terraform.io/language/functions/yamldecode](https://www.terraform.io/language/functions/yamldecode)

Combine the to move databases map from locals to separate YAML files and load it. This will make it easier for users to manage list of required databases without need to understand Terraform code.

## Using Azure Terrafy to import existing resources to state and create Terraform definition
In your resource group create Storage account using GUI.

