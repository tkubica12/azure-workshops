resource "time_rotating" "entra" {
  count         = var.byo_app_registrations ? 0 : 1
  rotation_days = 180
}

resource "random_uuid" "stuff_read" {
  count = var.byo_app_registrations ? 0 : 1
}

resource "random_uuid" "stuff_write" {
  count = var.byo_app_registrations ? 0 : 1
}

resource "azuread_application" "web" {
  count        = var.byo_app_registrations ? 0 : 1
  display_name = "${local.base_name}-web"
  owners       = [data.azuread_client_config.current.object_id]

  password {
    display_name = "secret1"
    start_date   = time_rotating.entra[0].id
    end_date     = timeadd(time_rotating.entra[0].id, "4320h")
  }

  lifecycle {
    ignore_changes = [ web ]
  }
}

resource "azuread_application_redirect_uris" "web" {
  count          = var.byo_app_registrations ? 0 : 1
  application_id = azuread_application.web[0].id
  type           = "Web"

  redirect_uris = [
    "https://${azurerm_container_app.auth_entra_web.ingress[0].fqdn}${var.REDIRECT_PATH}"
  ]
}

resource "azuread_application" "api" {
  count           = var.byo_app_registrations ? 0 : 1
  display_name    = "${local.base_name}-api"
  owners          = [data.azuread_client_config.current.object_id]
  identifier_uris = [local.api_app_uri]

  api {
    mapped_claims_enabled          = true
    requested_access_token_version = 2

    oauth2_permission_scope {
      admin_consent_description  = "Allow the application to read stuff on user behalf."
      admin_consent_display_name = "Stuff.Read"
      enabled                    = true
      id                         = random_uuid.stuff_read[0].result
      type                       = "User"
      user_consent_description   = "Allow the application to read stuff on your behalf."
      user_consent_display_name  = "Stuff.Read"
      value                      = "Stuff.Read"
    }

    oauth2_permission_scope {
      admin_consent_description  = "Allow the application to write stuff on user behalf."
      admin_consent_display_name = "Stuff.Write"
      enabled                    = true
      id                         = random_uuid.stuff_write[0].result
      type                       = "User"
      user_consent_description   = "Allow the application to write stuff on your behalf."
      user_consent_display_name  = "Stuff.Write"
      value                      = "Stuff.Write"
    }
  }

  password {
    display_name = "secret1"
    start_date   = time_rotating.entra[0].id
    end_date     = timeadd(time_rotating.entra[0].id, "4320h")
  }
}

resource "azuread_application" "apim" {
  count        = var.byo_app_registrations ? 0 : 1
  display_name = "${local.base_name}-apim"
  owners       = [data.azuread_client_config.current.object_id]

  password {
    display_name = "secret1"
    start_date   = time_rotating.entra[0].id
    end_date     = timeadd(time_rotating.entra[0].id, "4320h")
  }
}

resource "azuread_application" "background" {
  count        = var.byo_app_registrations ? 0 : 1
  display_name = "${local.base_name}-background"
  owners       = [data.azuread_client_config.current.object_id]

  required_resource_access {
    resource_app_id = var.byo_app_registrations ? var.app_registrations["api"]["client_id"] : azuread_application.api[0].client_id

    resource_access {
      id   = var.byo_app_registrations ? null : random_uuid.stuff_read[0].result
      type = "Scope"
    }
  }

  password {
    display_name = "secret1"
    start_date   = time_rotating.entra[0].id
    end_date     = timeadd(time_rotating.entra[0].id, "4320h")
  }
}

