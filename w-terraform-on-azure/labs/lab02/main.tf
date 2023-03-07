// Resource Group
resource "azurerm_resource_group" "demo" {
  name     = "yourname-lab2rg"
  location = "westeurope"
}

module "sql" {
  source = "./modules/azuresql"
  prefix = "tomas"
}
