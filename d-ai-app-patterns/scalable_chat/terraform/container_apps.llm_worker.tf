resource "azurerm_container_app" "llm_worker" {
  name                         = "ca-llmworker-${local.base_name}"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  identity {
    type = "SystemAssigned"
  }

  template {
    min_replicas = 0
    max_replicas = 10

    container {
      name   = "llm-worker"
      image  = "ghcr.io/tkubica12/azure-workshops/d-ai-app-patterns-scalable-chat-llm-worker:latest"
      cpu    = 0.5
      memory = "1.0Gi"

      env {
        name  = "SERVICEBUS_FULLY_QUALIFIED_NAMESPACE"
        value = "${azurerm_servicebus_namespace.main.name}.servicebus.windows.net"
      }
      env {
        name  = "SERVICEBUS_USER_MESSAGES_TOPIC"
        value = azurerm_servicebus_topic.user_messages.name
      }
      env {
        name  = "SERVICEBUS_USER_MESSAGES_SUBSCRIPTION"
        value = azurerm_servicebus_subscription.worker_service.name
      }
      env {
        name  = "SERVICEBUS_TOKEN_STREAMS_TOPIC"
        value = azurerm_servicebus_topic.token_streams.name
      }
      env {
        name  = "MAX_CONCURRENCY"
        value = "100"
      }
      env {
        name  = "LOG_LEVEL"
        value = "INFO"
      }
      env {
        name  = "APPLICATIONINSIGHTS_CONNECTION_STRING"
        value = azurerm_application_insights.main.connection_string
      }
      env {
        name  = "OTEL_SERVICE_NAME"
        value = "llm-worker"
      }
    }
    custom_scale_rule {
      name             = "service-bus-topic-scale-rule"
      custom_rule_type = "azure-servicebus"
      metadata = {
        topicName        = azurerm_servicebus_topic.user_messages.name
        subscriptionName = azurerm_servicebus_subscription.worker_service.name
        namespace        = azurerm_servicebus_namespace.main.name
        messageCount     = "5"
      }
    }
  }
}
