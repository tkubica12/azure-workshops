// In my case I will use just connected AKS so do not need this

# resource "azurerm_machine_learning_compute_instance" "demo" {
#   name                          = "demo"
#   location                      = azurerm_resource_group.demo.location
#   machine_learning_workspace_id = azurerm_machine_learning_workspace.demo.id
#   virtual_machine_size          = "Standard_D2as_v4"
#   authorization_type            = "personal"
#   local_auth_enabled            = false
# }
