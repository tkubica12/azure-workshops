resource "azurerm_container_app" "auth_entra_web" {
  name                         = "ca-auth-entra-web"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  ingress {
    external_enabled = true
    target_port      = 5000

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 0
    max_replicas = 1

    container {
      name   = "myapp"
      image  = "ghcr.io/tkubica12/jnt-apim-hackathon/auth_entra_web:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "REDIRECT_PATH"
        value = var.REDIRECT_PATH
      }

      env {
        name  = "AUTHORITY"
        value = local.authority
      }

      env {
        name  = "MAIN_CLIENT_ID"
        value = local.main_app.client_id
      }

      env {
        name  = "MAIN_CLIENT_SECRET"
        value = local.main_app.client_secret
      }

      env {
        name  = "BACKGROUND_CLIENT_ID"
        value = local.background_app.client_id
      }

      env {
        name  = "BACKGROUND_CLIENT_SECRET"
        value = local.background_app.client_secret
      }

      env {
        name  = "ENTRA_SCOPES"
        value = jsonencode(local.entra_scopes)
      }

      env {
        name  = "API_SCOPES"
        value = jsonencode(local.api_scopes)
      }

      env {
        name  = "API_SCOPES_CLIENT_CRED_FLOW"
        value = jsonencode(local.api_scopes_client_cred_flow)
      }

      env {
        name  = "GRAPH_API_ENDPOINT"
        value = local.graph_api_endpoint
      }

      env {
        name  = "CUSTOM_API_ENDPOINT"
        value = "https://${azurerm_container_app.auth_entra_api.ingress[0].fqdn}"
      }

      env {
        name = "CUSTOM_API_APIM_PASSTHROUGH_ENDPOINT"
        value = "${azurerm_api_management.main.gateway_url}/passthrough"
      }

      env {
        name = "CUSTOM_API_APIM_ONBEHALF_ENDPOINT"
        value = "${azurerm_api_management.main.gateway_url}/onbehalf"
      }

      env {
        name = "CUSTOM_API_APIM_REMOVEAUTH_ENDPOINT"
        value = "${azurerm_api_management.main.gateway_url}/removeauth"
      }

      env {
        name  = "PAGE_NAME"
        value = var.PAGE_NAME
      }

      env {
        name  = "FLASK_SECRET_KEY"
        value = var.FLASK_SECRET_KEY
      }
    }
  }
}
