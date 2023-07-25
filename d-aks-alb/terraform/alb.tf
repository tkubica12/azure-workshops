resource "azurerm_user_assigned_identity" "alb" {
  name                = "alb"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
}

# data "azurerm_resource_group" "mc" {
#   name = azurerm_kubernetes_cluster.main.node_resource_group_id
# }

resource "azurerm_role_assignment" "alb_mcrg_reader" {
  scope                = azurerm_kubernetes_cluster.main.node_resource_group_id
  role_definition_name = "Reader"
  principal_id         = azurerm_user_assigned_identity.alb.principal_id
}

resource "azurerm_role_assignment" "alb_mcrg_configmanager" {
  scope                = azurerm_kubernetes_cluster.main.node_resource_group_id
  role_definition_name = "AppGw for Containers Configuration Manager"
  principal_id         = azurerm_user_assigned_identity.alb.principal_id
}

resource "azurerm_role_assignment" "alb_subnet" {
  scope                = azurerm_subnet.alb.id
  role_definition_name = "Network Contributor"
  principal_id         = azurerm_user_assigned_identity.alb.principal_id
}

resource "azurerm_federated_identity_credential" "alb" {
  name                = "aks"
  resource_group_name = azurerm_resource_group.main.name
  audience            = ["api://AzureADTokenExchange"]
  issuer              = azurerm_kubernetes_cluster.main.oidc_issuer_url
  parent_id           = azurerm_user_assigned_identity.alb.id
  subject             = "system:serviceaccount:azure-alb-system:alb-controller-sa"
}

resource "helm_release" "alb" {
  name       = "alb-controller"
  repository = "oci://mcr.microsoft.com/application-lb/charts"
  chart      = "alb-controller"
  version    = "0.4.023921"

  set {
    name  = "albController.podIdentity.clientID"
    value = azurerm_user_assigned_identity.alb.client_id
  }
}

resource "helm_release" "demo" {
  name         = "demo"
  chart        = "../charts/demo"
  version      = "0.1.0"
  force_update = true

  set {
    name  = "ALB_SUBNET_ID"
    value = azurerm_subnet.alb.id
  }

  set {
    name  = "test"
    value = "TEST7"
  }
}
