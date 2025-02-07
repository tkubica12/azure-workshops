# # ...existing code...

# resource "azurerm_api_management_named_value" "openai_api_uami" {
#   name                = "uami-client-id"  
#   resource_group_name = azurerm_resource_group.main.name
#   api_management_name = azurerm_api_management.main.name
#   display_name        = "uami-client-id"
#   secret              = true
#   value               = var.managed_identity_client_id
# }

# resource "azurerm_api_management_named_value" "openai_api_entra" {
#   name                = "entra-auth" 
#   resource_group_name = azurerm_resource_group.main.name
#   api_management_name = azurerm_api_management.main.name
#   display_name        = "entra-auth"
#   secret              = false
#   value               = var.entra_auth
# }

# resource "azurerm_api_management_named_value" "openai_api_client" {
#   name                = "client-id" 
#   resource_group_name = azurerm_resource_group.main.name
#   api_management_name = azurerm_api_management.main.name
#   display_name        = "client-id"
#   secret              = true
#   value               = azurerm_user_assigned_identity.main.client_id
# }

# resource "azurerm_api_management_named_value" "openai_api_tenant" {
#   name                = "tenant-id"
#   resource_group_name = azurerm_resource_group.main.name
#   api_management_name = azurerm_api_management.main.name
#   display_name        = "tenant-id"
#   secret              = true
#   value               = data.azurerm_client_config.current.tenant_id
# }

# resource "azurerm_api_management_named_value" "openai_api_audience" {
#   name                = "audience"  
#   resource_group_name = azurerm_resource_group.example.name
#   api_management_name = azurerm_api_management.example.name
#   display_name        = "audience"
#   secret              = true
#   value               = var.audience
# }
