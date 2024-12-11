locals {
  base_name        = "${replace(var.prefix, "_", "-")}-${random_string.main.result}"
  base_name_nodash = replace(local.base_name, "-", "")

  main_app = {
    client_id     = var.byo_app_registrations ? var.app_registrations["main"]["client_id"] : azuread_application.web[0].client_id
    client_secret = var.byo_app_registrations ? var.app_registrations["main"]["client_secret"] : (tolist(azuread_application.web[0].password)[0].value)
  }
  api_app = {
    client_id     = var.byo_app_registrations ? var.app_registrations["api"]["client_id"] : azuread_application.api[0].client_id
    client_secret = var.byo_app_registrations ? var.app_registrations["api"]["client_secret"] : (tolist(azuread_application.api[0].password)[0].value)
  }
  background_app = {
    client_id     = var.byo_app_registrations ? var.app_registrations["background"]["client_id"] : azuread_application.background[0].client_id
    client_secret = var.byo_app_registrations ? var.app_registrations["background"]["client_secret"] : (tolist(azuread_application.background[0].password)[0].value)
  }
  apim_app = {
    client_id     = var.byo_app_registrations ? var.app_registrations["apim"]["client_id"] : azuread_application.apim[0].client_id
    client_secret = var.byo_app_registrations ? var.app_registrations["apim"]["client_secret"] : (tolist(azuread_application.apim[0].password)[0].value)
  }

  api_app_uri                 = var.byo_app_registrations ? var.app_registrations["api"]["uri"] : "api://${local.base_name}-api"
  entra_scopes                = ["User.Read"]
  api_scopes                  = ["${local.api_app_uri}/Stuff.Read"]
  api_scopes_client_cred_flow = ["${local.api_app_uri}/.default"]
  graph_api_endpoint          = "https://graph.microsoft.com/v1.0/me"
  authority                   = "https://login.microsoftonline.com/${var.TENANT_ID}"
}
