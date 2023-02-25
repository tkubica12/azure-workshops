resource "kubernetes_secret" "sbkey" {
  metadata {
    name      = "sbkey"
    namespace = "default"
  }

  data = {
    servicebus-connectionstring = azurerm_servicebus_queue_authorization_rule.demo.primary_connection_string
  }

  type = "kubernetes.io/Opaque"
}

resource "kubernetes_secret" "mysecrets" {
  metadata {
    name      = "mysecrets"
    namespace = "default"
  }

  data = {
    password = var.password
  }

  type = "kubernetes.io/Opaque"
}


resource "kubernetes_namespace" "aso" {
  metadata {
    name = "azureserviceoperator-system"
  }
  lifecycle {
    ignore_changes = [metadata]
  }
}

resource "kubernetes_secret" "aso" {
  metadata {
    name      = "aso-controller-settings"
    namespace = kubernetes_namespace.aso.metadata[0].name
  }

  data = {
    AZURE_SUBSCRIPTION_ID = var.AZURE_SUBSCRIPTION_ID
    AZURE_TENANT_ID       = var.AZURE_TENANT_ID
    AZURE_CLIENT_ID       = var.AZURE_CLIENT_ID
    AZURE_CLIENT_SECRET   = var.AZURE_CLIENT_SECRET
  }

  type = "kubernetes.io/Opaque"
}

resource "kubernetes_namespace" "arc" {
  metadata {
    name = "arc"
  }
  lifecycle {
    ignore_changes = [metadata]
  }
}

resource "kubernetes_secret" "sql1" {
  metadata {
    name      = "sql1-login-secret"
    namespace = kubernetes_namespace.arc.metadata[0].name
  }

  data = {
    username = "labuser"
    password = var.password
  }

  type = "kubernetes.io/Opaque"
}

resource "kubernetes_secret" "metricsui" {
  metadata {
    name      = "metricsui-admin-secret"
    namespace = kubernetes_namespace.arc.metadata[0].name
  }

  data = {
    username = "labuser"
    password = var.password
  }

  type = "kubernetes.io/Opaque"
}

resource "kubernetes_secret" "logsui" {
  metadata {
    name      = "logsui-admin-secret"
    namespace = kubernetes_namespace.arc.metadata[0].name
  }

  data = {
    username = "labuser"
    password = var.password
  }

  type = "kubernetes.io/Opaque"
}
