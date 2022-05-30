# Workshop - Terraform on Azure


# Lab 1 - Get started with Terraform on Azure
In this lab we will setup Terraform and deploy our first few resources.

[guide](./docs/01-getStarted.md)

# Lab 2 - Create module for repeatable deployment of Azure SQL
In this lab we will introduce modules and work on Azure SQL module. We will also introduce AzApi for situation when AzureRm Terraform provider does not support some newer Azure feature (eg. something in preview).

[guide](./docs/02-sqlModule.md)

# Lab 3 - More advanced concepts: versioning, conditions, structure inputs and abstractions, cycles
In this lab we will start from two modules - one for Azure SQL and one for Azure WebApp and introduce concepts such as conditions, loops, your own abstractions and versioning.

[guide](./docs/03-advancedContepts.md)

# Lab 4 - Add layer of abstractions for environments

# Lab 5 - Automate deployment and processes with GitHub