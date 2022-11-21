resource "azurerm_firewall_policy" "main" {
  name                = "${var.name}-fwpolicy"
  location            = var.location
  resource_group_name = var.rg_name
  sku                 = "Standard"
}

resource "azurerm_firewall_policy_rule_collection_group" "main" {
  name               = "main-group"
  firewall_policy_id = azurerm_firewall_policy.main.id
  priority           = 500

  # application_rule_collection {
  #   name     = "app_rule_collection1"
  #   priority = 500
  #   action   = "Deny"
  #   rule {
  #     name = "app_rule_collection1_rule1"
  #     protocols {
  #       type = "Http"
  #       port = 80
  #     }
  #     protocols {
  #       type = "Https"
  #       port = 443
  #     }
  #     source_addresses  = ["10.0.0.1"]
  #     destination_fqdns = ["*.microsoft.com"]
  #   }
  # }

  network_rule_collection {
    name     = "ms_services"
    priority = 400
    action   = "Allow"
    rule {
      name             = "ms_services"
      protocols        = ["TCP", "UDP"]
      source_addresses = ["0.0.0.0/0"]
      destination_addresses = [
        "AzureActiveDirectory",
        "AzureSiteRecovery",
        "GuestAndHybridManagement"
      ]
      destination_ports = ["80", "443"]
    }
  }
}
