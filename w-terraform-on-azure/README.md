# Workshop - Terraform on Azure


# Lab 1 - Get started with Terraform on Azure
In this lab we will setup Terraform and deploy our first few resources.

[guide](./docs/01-getStarted.md)

# Lab 2 - Create module for repeatable deployment of Azure SQL
In this lab we will introduce modules and work on Azure SQL module. We will also introduce AzApi for situation when AzureRm Terraform provider does not support some newer Azure feature (eg. something in preview).

[guide](./docs/02-module.md)

# Lab 3 - More advanced concepts: versioning, conditions, structure inputs and abstractions, cycles
In this lab we will introduce concepts such as conditions, loops, your own abstractions, versioning and more.

[guide](./docs/03-advancedContepts.md)

# Lab 4 - Add layer of abstractions for environments
We have modularized out template to create reusable components, but whole project (application) should also be versatile enough to be used in multiple environments such as prod, staging, dev or even ephemeral (environment to be spin up when needed and killed after tests are done).

[guide](./docs/04-environments.md)

# Lab 5 - Automate deployment and processes with GitHub
TBD