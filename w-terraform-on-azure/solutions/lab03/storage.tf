resource "azurerm_storage_account" "example" {
  name                             = "tomasteststore123"
  resource_group_name              = azurerm_resource_group.demo.name
  location                         = azurerm_resource_group.demo.location
  account_tier                     = "Standard"
  account_replication_type         = "LRS"
  min_tls_version                  = "TLS1_0"
  cross_tenant_replication_enabled = true

  network_rules {
    default_action = "Deny"
    ip_rules       = ["1.2.3.4"]
  }
}
