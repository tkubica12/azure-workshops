# Lab 3 - More advanced concepts: versioning, conditions, structure inputs and abstractions, cycles

## Conditionals
As first tak we will want make our Azure SQL module more universal by adding configuration of auditing to Azure Monitor (Log Analytics workspace is being created in root module already), but conditionally. We want to configure this for our production deployments, but not for dev environments to save costs. We need to make sure module can be parametrized to deploy auditing only when asked for.

Here are resources to be placed in module (do not forget to also declare logWorkspaceId variable):

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
Often you need to create the same resource multiple times, call module multiple times or repeat one structure inside resource. Terraform supports loops on all mentioned levels. It is often preferable to use for each with map so keys are fixed and predictable. Using simple for loop with index number might have negative side effects eg. if you insert item in array (than it might renumber therefore recreate all resources which might cause downtime - eg. when touching existing firewall rules).

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

## Import existing resources to state and create Terraform definition
Currently there is no easy 100% reliable to automatically convert clicked resources into nice working Terraform code. Check out project [Azure Terrafy](https://github.com/Azure/aztfy/releases) that provides simplification of bellow proces, but is not as time of writing this ready for safe production use. We will use traditional manual way. 

Main purpose of this is to make "unmanaged" resource part of Terraform so it can be managed by it from now on. Note with stateless resources it is usually much faster to create template from scratch, but there are scenarios when existing resources simply cannot be recreated, because they contain some important state (eg. database) or are in active use (eg. VPN connection to on-premises).

Use Azure CLI to create "unmanaged" resource:

```bash
az storage account create -n tomasteststore123 -g lab03rg --sku Standard_LRS --default-action Deny --bypass AzureServices --allow-cross-tenant-replication true
az storage account network-rule add -g lab03rg --account-name tomasteststore123 --ip-address 1.2.3.4
```

Create storage.tf file with this content (just to start - we have intentionally left out some parts):

```
resource "azurerm_storage_account" "example" {
  name                     = "tomasteststore123"
  resource_group_name      = azurerm_resource_group.demo.name
  location                 = azurerm_resource_group.demo.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
```

If you now run ```terraform apply -auto-approve``` you will see Terraform is trying to create this resource since it has no state for it and this will fail.

Lets import this resource now 

```
terraform import azurerm_storage_account.example $(az storage account show -n tomasteststore123 -g lab03rg --query id -o tsv)
```

With resource imported let's now run ```terraform plan```. If we have typed template correctly, we should see no changes are needed. If Terraform wants to do any change on our resource keep tuning your template until it is correctly reflecting your existing resource.

Only when done with this, remove resource lock and run ```terraform apply``` - from now on this resource is managed by Terraform.

Note: situation can get much more complicated with complex resources with a lot of interactions. Therefore use import feature only when fixing some issue or when you need to import something critically important. Otherwise is better to create new infrastructure managed by Terraform from day one. While Azure Terrafy can significantly simplify this process it will probably never be 100% reliable and templates produced still need to be modified to include best practices (such as no hardcoded values etc.).

## Modules versioning and remote reference
Modules should be version controlled and reusable so used by multiple projects so should be stored in central repository (you may use mono-repo style and put all modules in single repo or use repo per module - both strategies has certain advantages). Since modules need to evolve and might introduce breaking changes it is important for projects to be able to reference specific version they want to use.

1. Create new public repository in GitHub
2. Store your modules folder there and commit
3. Create GitHub Release and call this version 0.0.1 (in other Git systems use Git tag)
4. When calling module in your root reference remote git now and use "ref" to lock it to version 0.0.1
   ```
   source = "github.com/myorg/mymodulesrepo//modules?ref=0.0.1" 
   ```
5. Run ```terraform init``` to download module and you are ready to apply

## Working with multiple roots
Suppose we need to have different root resources - eg. network was deployed with infrastructure template and this is different team from application projects that are just using shared resource. What if we need read attribute of some resources that has been deployed with someone elses template? Sure we can pass value as argument, but what are other options?

### Referencing existing resource with "data" objects
Create another root template by creating folder and with following provider and just local state:

```
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
    template_deployment {
      delete_nested_items_during_deletion = false
    }
    key_vault {
      purge_soft_delete_on_destroy    = true
      recover_soft_deleted_key_vaults = false
    }
  }
}
```

Initialize. Let's say we need to output IP range of existing VNET.

```
locals {
  vnetName = "myvnet"
  vnetResoucreGroupName = "lab03rg"
}

data "azurerm_virtual_network" "example" {
  name                = local.vnetName
  resource_group_name = local.vnetResoucreGroupName
}

output "ipRangeFromData" {
  value = data.azurerm_virtual_network.example.address_space
}
```

### Referencing existing state
Output of one template (eg. network infrastructure) can be used with other templates using various techniques:
- You can directly reference remote state as described [here](https://www.terraform.io/language/state/remote-state-data), but it is consider unsecure as you get access to full state file which might include sensitive information.
- If you use Terraform Cloud you can leverage specific feature to securely access outputs.
- When running everything in CI/CD such as GitHub Actions store outputs as artifacts or commit non-sensitive values to repo.
- Store secrets in Azure Key Vault. 
  - If possible get rid of secrets all together by using Managed Identities everywhere.
  - If you need secrets prefer accessing it from application rather than loading to Terraform so it is not stored in tfstate file.
  - If resource does require to specify password in Terraform, load it from Key Vault - it is still much more secure than passing things as arguments.

Here is how you can load secret from Key Vault to Terraform and use it (we are outputing it here, even not display on screen -> try to never do this):

```
data "azurerm_key_vault_secret" "example" {
  name         = "tomdb1-rwcnpumsoxaf"
  key_vault_id = "/subscriptions/a0f4a733-4fce-4d49-b8a8-d30541fc1b45/resourceGroups/lab03rg/providers/Microsoft.KeyVault/vaults/ldsbpesnqutzmjei"
}

output "secret_value" {
  value     = data.azurerm_key_vault_secret.example.value
  sensitive = true
}
```

Get output by calling ```terraform output secret_value```

