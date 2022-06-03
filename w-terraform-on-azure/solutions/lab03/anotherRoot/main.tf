locals {
  vnetName = "myvnet"
  vnetResoucreGroupName = "lab03rg"
}

data "azurerm_virtual_network" "example" {
  name                = local.vnetName
  resource_group_name = local.vnetResoucreGroupName
}

data "azurerm_key_vault_secret" "example" {
  name         = "tomdb1-rwcnpumsoxaf"
  key_vault_id = "/subscriptions/a0f4a733-4fce-4d49-b8a8-d30541fc1b45/resourceGroups/lab03rg/providers/Microsoft.KeyVault/vaults/ldsbpesnqutzmjei"
}

output "secret_value" {
  value     = data.azurerm_key_vault_secret.example.value
  sensitive = true
}

output "ipRangeFromData" {
  value = data.azurerm_virtual_network.example.address_space
}