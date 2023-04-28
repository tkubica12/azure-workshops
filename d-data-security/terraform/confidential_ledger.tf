resource "azurerm_confidential_ledger" "main" {
  count               = var.enable_ledger ? 1 : 0
  name                = random_string.main.result
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  ledger_type         = "Private"

  azuread_based_service_principal {
    principal_id     = data.azurerm_client_config.current.object_id
    tenant_id        = data.azurerm_client_config.current.tenant_id
    ledger_role_name = "Administrator"
  }
}
