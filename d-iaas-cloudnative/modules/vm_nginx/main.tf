module "naming" {
  source = "Azure/naming/azurerm"
  suffix = [var.prefix]
}