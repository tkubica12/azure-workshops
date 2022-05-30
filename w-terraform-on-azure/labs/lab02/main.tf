// Resource Group
resource "azurerm_resource_group" "demo" {
  name     = "lab01rg"
  location = "westeurope"
}

module "sql" {
  source = "./modules/azuresql"
  prefix = "tomas"
}
