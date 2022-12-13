// AKS cluster
resource "azurerm_kubernetes_cluster" "demo" {
  count               = var.deploy_aks ? 1 : 0
  name                = "ml-aks"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  dns_prefix          = "ml-aks"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_B2ms"
  }

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.aks.id,
    ]
  }

  kubelet_identity {
    client_id                 = azurerm_user_assigned_identity.aks.client_id
    object_id                 = azurerm_user_assigned_identity.aks.principal_id
    user_assigned_identity_id = azurerm_user_assigned_identity.aks.id
  }

  depends_on = [
    azurerm_role_assignment.aks
  ]
}

// Resource required to attach Kubernetes to Azure ML workspace
resource "azurerm_relay_namespace" "demo" {
  count               = var.deploy_aks ? 1 : 0
  name                = "relay-${random_string.random.result}"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  sku_name            = "Standard"
}

resource "azurerm_relay_hybrid_connection" "demo" {
  count                         = var.deploy_aks ? 1 : 0
  name                          = "ml-aks"
  resource_group_name           = azurerm_resource_group.demo.name
  relay_namespace_name          = azurerm_relay_namespace.demo[0].name
  requires_client_authorization = true
}


resource "azurerm_relay_hybrid_connection_authorization_rule" "demo" {
  count                  = var.deploy_aks ? 1 : 0
  name                   = "azureml_rw"
  resource_group_name    = azurerm_resource_group.demo.name
  hybrid_connection_name = azurerm_relay_hybrid_connection.demo[0].name
  namespace_name         = azurerm_relay_namespace.demo[0].name


  listen = true
  send   = true
  manage = true
}

resource "azurerm_servicebus_namespace" "demo" {
  count               = var.deploy_aks ? 1 : 0
  name                = "sb-${random_string.random.result}"
  location            = azurerm_resource_group.demo.location
  resource_group_name = azurerm_resource_group.demo.name
  sku                 = "Standard"
}

resource "azurerm_servicebus_topic" "computestate" {
  count                 = var.deploy_aks ? 1 : 0
  name                  = "computestate-updatedby-computeprovider"
  namespace_id          = azurerm_servicebus_namespace.demo[0].id
  default_message_ttl   = "P60D"
  max_size_in_megabytes = 5120
}

resource "azurerm_servicebus_subscription" "computestate" {
  count               = var.deploy_aks ? 1 : 0
  name                = "compute-scheduler-computestate"
  topic_id            = azurerm_servicebus_topic.computestate[0].id
  max_delivery_count  = 1
  lock_duration       = "PT30S"
  default_message_ttl = "P14D"
}

resource "azurerm_servicebus_topic" "jobstate" {
  count                 = var.deploy_aks ? 1 : 0
  name                  = "jobstate-updatedby-computeprovider"
  namespace_id          = azurerm_servicebus_namespace.demo[0].id
  default_message_ttl   = "P60D"
  max_size_in_megabytes = 5120
}

resource "azurerm_servicebus_subscription" "jobstate" {
  count               = var.deploy_aks ? 1 : 0
  name                = "compute-scheduler-computestate"
  topic_id            = azurerm_servicebus_topic.jobstate[0].id
  max_delivery_count  = 1
  lock_duration       = "PT30S"
  default_message_ttl = "P1D"
}

resource "azurerm_servicebus_namespace_authorization_rule" "demo" {
  count        = var.deploy_aks ? 1 : 0
  name         = "full"
  namespace_id = azurerm_servicebus_namespace.demo[0].id
  listen       = true
  send         = true
  manage       = true
}

resource "azapi_resource" "azuremlextension" {
  count     = var.deploy_aks ? 1 : 0
  type      = "Microsoft.KubernetesConfiguration/extensions@2022-03-01"
  name      = "aml"
  parent_id = azurerm_kubernetes_cluster.demo[0].id

  body = jsonencode({
    properties = {
      extensionType = "microsoft.azureml.kubernetes"
      releaseTrain  = "stable"
      scope = {
        cluster = {
          releaseNamespace = "azureml"
        }
      }
      configurationSettings = {
        enableTraining                                                      = "True"
        enableInference                                                     = "True"
        inferenceRouterServiceType                                          = "LoadBalancer"
        allowInsecureConnections                                            = "True"
        inferenceLoadBalancerHA                                             = "False"
        clusterPurpose                                                      = "DevTest"
        cluster_name                                                        = azurerm_kubernetes_cluster.demo[0].id
        domain                                                              = "${azurerm_resource_group.demo.location}.cloudapp.azure.com"
        location                                                            = azurerm_resource_group.demo.location
        jobSchedulerLocation                                                = azurerm_resource_group.demo.location
        cluster_name_friendly                                               = azurerm_kubernetes_cluster.demo[0].name
        "relayserver.hybridConnectionResourceID"                            = azurerm_relay_hybrid_connection.demo[0].id
        "relayserver.hybridConnectionName"                                  = azurerm_relay_hybrid_connection.demo[0].name
        "servicebus.resourceID"                                             = azurerm_servicebus_namespace.demo[0].id
        "servicebus.topicSubMapping.computestate-updatedby-computeprovider" = "compute-scheduler-computestate"
        "servicebus.topicSubMapping.jobstate-updatedby-computeprovider"     = "compute-scheduler-jobstate"
        clusterId                                                           = azurerm_kubernetes_cluster.demo[0].id
        "prometheus.prometheusSpec.externalLabels.cluster_name"             = azurerm_kubernetes_cluster.demo[0].id
      }
      configurationProtectedSettings = {
        relayServerConnectionString         = azurerm_relay_hybrid_connection_authorization_rule.demo[0].primary_connection_string
        "relayserver.relayConnectionString" = azurerm_relay_hybrid_connection_authorization_rule.demo[0].primary_connection_string
        serviceBusConnectionString          = azurerm_servicebus_namespace_authorization_rule.demo[0].primary_connection_string
        "servicebus.connectionString"       = azurerm_servicebus_namespace_authorization_rule.demo[0].primary_connection_string
      }
    }
    }
  )

  lifecycle {
    ignore_changes = [
      body
    ]
  }
}
