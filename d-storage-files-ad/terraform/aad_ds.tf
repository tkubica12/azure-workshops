resource "azurerm_active_directory_domain_service" "main" {
  name                = "tkubica.biz"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  domain_name           = "tkubica.biz"
  sku                   = "Standard"
  filtered_sync_enabled = false

  initial_replica_set {
    subnet_id = azurerm_subnet.ds.id
  }

  notifications {
    notify_dc_admins      = true
    notify_global_admins  = true
  }

  security {
    sync_kerberos_passwords = true
    sync_ntlm_passwords     = true
    sync_on_prem_passwords  = true
  }

  depends_on = [
    azurerm_subnet_network_security_group_association.ds,
    azuread_service_principal.main
  ]
}

resource "azuread_service_principal" "main" {
  application_id = "2565bd9d-da50-47d4-8b85-4c97f669dc36" // published app for domain services
}

resource "random_password" "dc_admin" {
  length = 64
}

resource "azuread_user" "dc_admin" {
  user_principal_name = "dcadmin@tkubica.biz"
  display_name        = "AADDS DC Administrator"
  password            = random_password.dc_admin.result
}

resource "azuread_group" "dc_admins" {
  display_name     = "AAD DC Administrators"
  security_enabled = true
}


resource "azuread_group_member" "dc_admin" {
  group_object_id  = azuread_group.dc_admins.object_id
  member_object_id = azuread_user.dc_admin.object_id
}



