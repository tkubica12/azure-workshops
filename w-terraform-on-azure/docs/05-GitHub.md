# Lab 5 - Automate deployment and processes with GitHub
We will no add process, collaboration and automation to our Infrastructure as Code project. This guide uses [GitHub CLI](https://cli.github.com/), but feel free to use GUI or review what CLI did on GitHub.com.

## Authenticate to GitHub, create repository and push initial code
Create local folder outside of your azure-workshops folder and copy content of w-terraform-on-azure/labs/lab05/* to it.

```bash
# Login
gh auth login 

# Go to your home folder
cd ~

# Create repo
gh repo create myiactest -y --public
cd ~/myiactest

# Copy initial files (change path to reflect your environment)
cp "/mnt/c/Users/tokubica/OneDrive - Microsoft/git/azure-workshops/w-terraform-on-azure/labs/lab05/" -RTv .

# Make initial commit
git add -A
git commit -m "Initial commit"
git push --set-upstream origin master
```

Reopen this folder in your VS Code so you see proper files and you can use VS Code to push code changes etc.

## Version control
Let's deploy production as it is. Do not forget to change providers.tf file in your projects/myproject/environments/prod/ folder to reflect your storage account to store state.

```bash
cd ./projects/myproject/environments/prod/
terraform init
terraform plan
terraform apply -auto-approve
```

Database includes tag that you can check in Azure portal - we will use this to simulate changes to our code. Go to modules/azuresql/main.tf, locate database definition and change value of the tag.

```
// SQL Database
resource "azurerm_mssql_database" "test" {
  name           = var.dbName
  server_id      = azurerm_mssql_server.module.id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  read_scale     = var.readScale
  sku_name       = var.skuName
  zone_redundant = var.zoneRedundant

  tags = {
    moduleVersion = "0.0.2"
  }
}
```

Commit this change and push it to GitHub. Than deploy changes to infrastructure.

```bash
git add -A
git commit -m "Change version tag in SQL database"
git push
terraform apply -auto-approve
```

See this commit in GitHub GUI, VS Code or using CLI - you can see exactly what was changed and who did the change.

```bash
git log -p
```

Suppose you need to run terraform again to undo changes in latest commit. You can go back in time a apply.

```bash
# Get commit id you want to go back to
git log --oneline

# Go back in time
git checkout 4a98332   # Note your hash is different!

# Apply infrastructure state
terraform apply -auto-approve
```

Now our latest declarative manifest is not what we actually run in production, but we will fix this later - we can use strategies such as relase tag pinning, branching, testing, rollforward strategy (fix this and release repaired version) or even delete bad commit from history (usualy not best thing to do).

Let's go back to present time and deploy again.

```bash
git switch -
terraform apply -auto-approve
```

## Organizing work and managing changes
Following "no work without reason" principle we will not do any changes unless it is requested by creating GitHub Issue. We will also assign ourselves to this task.

```bash
gh issue create --title "SQL module should include new LINK tag" --body "New standard LINK tags should be everywhere" --assignee "@me"
```

You are assigned to implement this change. Create new patch branch, author the change and create Pull Request (request to review and approve changes).

First create new branch (new paralel universe).

```bash
git checkout -b patch-sql-tag
```

Change modules/azuresql/main.tf to include new tag.

```
// SQL Database
resource "azurerm_mssql_database" "test" {
  name           = var.dbName
  server_id      = azurerm_mssql_server.module.id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  read_scale     = var.readScale
  sku_name       = var.skuName
  zone_redundant = var.zoneRedundant

  tags = {
    moduleVersion = "0.0.2"
    LINK = "something"
  }
}
```

Commit and push changes, create Pull Request (you can use gh CLI or GUI).

```bash
# Commit and push
git add -A
git commit -m "adding LINK tag to SQL database module"
git push --set-upstream origin patch-sql-tag

# Create PR and reference issue (#1 in my case)
gh pr create --title "SQL module should include new LINK tag" --body "Solves #1" --assignee "@me"
```

Open GitHub GUI and see your PR. Note you can have discussion, review changes or run automated actions such as tests (we will add this later). There might be policies configured to require another pair of eyes befor approval etc.

Accept changes and merge to master.

```bash
gh pr merge 2 --delete-branch --merge # your PR number might differ!
gh issue close 1 # your issue number might differ!
```

## Pinned module versions
Modules are components that are shared accross whole organization and sometimes might require changes that should not be automatically enrolled to every project due to potential negative effects:
- Team preparing module might have added new feature that increase cost of solution (eg. more extensive security logging enabled by default now) so it is not breaking change (module still works as its inputs have not changed), but it affects users
- Team preparing module need to do breaking change and redesign inputs so new features can be added (eg. ability to use serverless SKU for Azure SQL)

Our last change to SQL module is already commited (version 0.0.2 tag and LINK tag) so we can now flag this commit as Release so users can pin it in their projects.

```bash
gh release create module-sql-v0.0.2 --notes "Initial release of Azure SQL module"
```

For myproject we want to make sure that we reference specific version of SQL module, not latest one. Rather that loading module from local folder structure we will get it from GitHub using specific release tag. Modify your projects/main.tf file to reference your GitHub repo and release tag (note double // in path is not and error).

```
module "sql" {
  source            = "github.com/tkubica12/myiactest//modules/azuresql/?ref=module-sql-v0.0.2"
  for_each          = var.databases
  prefix            = each.key
  resourceGroupName = azurerm_resource_group.demo.name
  location          = azurerm_resource_group.demo.location
  keyVaultId        = azurerm_key_vault.kv.id
  subnetId          = azurerm_subnet.db.id
  dnsZoneId         = azapi_resource.privatednssql.id
  dbName            = each.value["dbName"]
  skuName           = each.value["skuName"]
}
```

You need to reinitialize Terraform and apply.

```bash
terraform init
terraform apply -auto-approve
```

You can now commit change to module (eg. changing LINK tag to something else) and apply terraform again - change in module will not affect your myproject infrastructure as module versioned is pinned to specific release, not latest development.

## Automation
In this task we will automate environment in following way:
- When PR is created with change in folder myproject, we willl
  - run ```terraform validate``` to check for syntax errors
  - run ```terraform plan``` against staging environment and capture plan output
- When changes in myproject folder get merged we will 
  - run ```terraform apply``` to staging environment consuming previously captured plan
  - run ```terraform plan``` against staging environment and capture plan output
- As manual trigger (dispatch) we will have ```terraform apply``` against production environment

Detailed steps TBD

  