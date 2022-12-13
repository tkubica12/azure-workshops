

resource "azurerm_application_insights" "demo" {
  name                = "appi-${random_string.random.result}"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  application_type    = "web"
}

resource "azurerm_key_vault" "demo" {
  name                      = "kv-${random_string.random.result}"
  location                  = azurerm_resource_group.demo.location
  resource_group_name       = azurerm_resource_group.demo.name
  tenant_id                 = data.azurerm_client_config.current.tenant_id
  sku_name                  = "standard"
  purge_protection_enabled  = false
  enable_rbac_authorization = true
}

resource "azurerm_storage_account" "demo" {
  name                     = "store${random_string.random.result}"
  location                 = azurerm_resource_group.demo.location
  resource_group_name      = azurerm_resource_group.demo.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_container_registry" "demo" {
  name                = "acr${random_string.random.result}"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  sku                 = "Basic"
  admin_enabled       = true
}

// Machine Learning workspace
resource "azurerm_machine_learning_workspace" "demo" {
  name                           = "aml-${random_string.random.result}"
  location                       = azurerm_resource_group.demo.location
  resource_group_name            = azurerm_resource_group.demo.name
  application_insights_id        = azurerm_application_insights.demo.id
  key_vault_id                   = azurerm_key_vault.demo.id
  storage_account_id             = azurerm_storage_account.demo.id
  container_registry_id          = azurerm_container_registry.demo.id
  primary_user_assigned_identity = azurerm_user_assigned_identity.aml.id
  public_network_access_enabled  = true

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.aml.id,
    ]
  }

  depends_on = [
    azurerm_role_assignment.aml
  ]
}
