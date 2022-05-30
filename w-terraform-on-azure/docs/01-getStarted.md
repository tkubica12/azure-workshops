# Lab 1 - Get started with Terraform on Azure
In this lab we will setup Terraform and deploy our first few resources.

## 1. Install Terraform on your Windows machine or in WSL (alternatively you can use Azure CloudShell which comes with Terraform preinstalled)
[https://learn.hashicorp.com/tutorials/terraform/install-cli](https://learn.hashicorp.com/tutorials/terraform/install-cli)

## 2. Install Azure CLI on your Windows machine or in WSL (alternatively you can use Azure CloudShell which comes with Azure CLI preinstalled). 
[https://docs.microsoft.com/en-us/cli/azure/install-azure-cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)

## 3. Install Visual Studio Code and extensions ms-azuretools.vscode-azureterraform and hashicorp.terraform

## 4. Login to Azure using ```az login``` command.

## 5. Go to labs/lab01 folder and check providers.tf file. 
Here we specify AzureRm provider and by default Terraform will reuse Azure CLI login token.

## 6. Initialize Terraform workspace with ```terraform init``` command. 
This will download providers and modules locally.

## 7. Create resource
Let's create our first object in Azure - Resource Group called ```lab01rg```. Look at Terraform documentation:

[https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/resource_group](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/resource_group)

Create additional tf file, eg. main.tf and using documentation and VS Code intellisense create resource for Resource Group in westeurope.

## 8. Investigate what Terraform plans to do using ```terraform plan```

## 9. Deploy your template using ```terraform apply -auto-approve```

## 10. Let Terraform create Virtual Network
See documenation here:
[https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_network](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_network)

To make things more readable let's use separate file for this called networking.tf.

Create Virtual Network with following parameters:
- Address space 10.0.0.0/16
- Do not include subnets directly, use separate resource, so we can easily reference it later: [https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/subnet](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/subnet)
- Subnet called ```vm-subnet``` with address prefix 10.0.0.0/24
- Subnet called ```db-subnet``` with address prefix 10.0.1.0/24
- Subnet called ```webapp-subnet``` with address prefix 10.0.2.0/24
- Reference location and resource group name from your RG definition

Plan and apply this with ```terraform plan``` and ```terraform apply -auto-approve```

## 11. Store state centrally
Now all Terraform state is stored on your PC so you are locked to your machine. We should store state in secure centralized location.

First delete existing resources using ```terraform destroy -auto-approve```

Create storage account in Azure and container called ```tfstate```

Modify your providers.tf file to use storage account as backend to store state>

```
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "myresourcegroup"
    storage_account_name = "mystorageaccount"
    container_name       = "tfstate"
    key                  = "lab01.tfstate"
    subscription_id      = "mysubscriptionid"
  }
}
```

Check content of state file in your storage account

## 12. Change actual state
Go to Azure and modify our resources - delete vm-subnet in your virtual network.

Re-run ```terraform plan``` - does Terraform indicate this subnet needs to be added back?

Re-run ```terraform apply -auto-approve``` to fix incosistencies.

## 12. Destroy resources
That is end of lab01. Destroy resources using ```teraform destroy -auto-approve```



