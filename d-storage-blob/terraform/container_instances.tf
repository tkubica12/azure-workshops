resource "azurerm_container_group" "container1" {
  name                = "container1"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  ip_address_type     = "None"
  dns_name_label      = random_string.storage.result
  os_type             = "Linux"

  container {
    name     = "container"
    image    = "mcr.microsoft.com/azure-cli:latest"
    cpu      = "0.5"
    memory   = "1.5"
    commands = ["tail", "-f", "/dev/null"]
  }

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.identity1.id
    ]
  }
}

resource "azurerm_container_group" "container2" {
  name                = "container2"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  ip_address_type     = "None"
  dns_name_label      = random_string.storage.result
  os_type             = "Linux"

  container {
    name     = "container"
    image    = "mcr.microsoft.com/azure-cli:latest"
    cpu      = "0.5"
    memory   = "1.5"
    commands = ["tail", "-f", "/dev/null"]
  }

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.identity2.id
    ]
  }
}
