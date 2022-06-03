# Lab 2 - Create module for repeatable deployment of Azure SQL
In this lab we will introduce modules and work on Azure SQL module. We will also introduce AzApi for situation when AzureRm Terraform provider does not support some newer Azure feature (eg. something in preview).

In you lab/lab02 you will find your module. At this point contains only generation of random name including configurable prefix, outputs this to root module. Change your providers.tf file to point to your storage and play with our module a bit.

```
terraform init
terraform plan
terraform apply -auto-approve
```

## SQL server

Here is snipped for your ```modules/azuresql/main.tf``` file with Azure SQL virtual server object. Module should be reusable so modify this so location and resource_group_name are referenced from input variable (see ```inputs.tf```). Than deploy (for now ignore hardcoded password).

```
resource "azurerm_mssql_server" "example" {
  name                         = "${var.prefix}-${random_string.name.result}"
  resource_group_name          = azurerm_resource_group.example.name
  location                     = azurerm_resource_group.example.location
  version                      = "12.0"
  administrator_login          = "azureuser"
  administrator_login_password = "Azure12345678!"
}
```

## Generated password
Hardcoded password? Bad idea. Let's use random provider to generate password. Follow documentation here: [https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/password](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/password)

## Store password in Key Vault
But how will applications get this password? Should we output it in Terraform? Much more secure will be to store it in Azure Key Vault:
- In your root module create Azure Key Vault (using random some random name) and in access policy set your current account with rights to Set, List and Get secrets (see [https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/key_vault](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/key_vault))
- Pass Key Vault ID as input to your azuresql module
- In azuresql module store password in Key Vault under key=nameofyourserver (see [https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/key_vault_secret](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/key_vault_secret))

## Private Endpoint and using AzApi provider when AzureRm does not support what you need
First we need to deploy Azure Private DNS zone for Private Endpoint of our Azure SQL. This is typicaly part of landing zone and networking, so for now let's create it in our root module.

Terraform AzureRm supports this, neverheless let's try alternative - using AzApi, which is just auto-generated API wrapper. We have already added this to your providers.tf file. Have a look at Azure API documentation: [https://docs.microsoft.com/en-us/rest/api/dns/privatedns/private-zones/create-or-update](https://docs.microsoft.com/en-us/rest/api/dns/privatedns/private-zones/create-or-update)

Resulting AzApi resource will look like this:

```
resource "azapi_resource" "privatednssql" {
  type      = "Microsoft.Network/privateDnsZones@2018-09-01"
  name      = "privatelink.database.windows.net"
  parent_id = azurerm_resource_group.demo.id
  location  = "global"
}
```

Then we need to link DNS zone to our VNET - for that we will use standard AzureRm provider: [https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/private_dns_zone_virtual_network_link](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/private_dns_zone_virtual_network_link)

Deploy.

As next step we need our azuresql module to get this zone ID as input with subnet ID and create Private Endpoint and DNS registration. Inputs of your module might look like this:

```
variable "subnetId" {
  type = string
}

variable "dnsZoneId" {
  type = string
}
```

Resource in your module:

```
// Create Private Endpoint and DNS zone group
resource "azurerm_private_endpoint" "azuresql" {
  name                = "${azurerm_mssql_server.example.name}-pe"
  resource_group_name = var.resourceGroupName
  location            = var.location
  subnet_id           = var.subnetId

  private_dns_zone_group {
    name                 = "${azurerm_mssql_server.example.name}-zonegroup"
    private_dns_zone_ids = [var.dnsZoneId]
  }

  private_service_connection {
    name                           = "${azurerm_mssql_server.example.name}-pconnection"
    private_connection_resource_id = azurerm_mssql_server.example.id
    is_manual_connection           = false
    subresource_names              = ["sqlServer"]
  }
}
```

Do not forget to pass subnetId and dnsZoneId as input when calling azuresql module.

## SQL Database
Add SQL Database to your module and for this to be reusable make sure you define key features such as size as inputs. In your input definition set reasonable defaults so when users do not what to use, they do not have to specify.

[https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/mssql_database](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/mssql_database)


## Destroy resources
We are on end of lab02, you can destroy all resources using ```terraform destroy -auto-approve``` now.
