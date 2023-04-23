resource "kubernetes_namespace_v1" "vulnerables" {
  metadata {
    name = "vulnerables"
  }
}

resource "kubernetes_pod_v1" "cve-2016-4977" {
  metadata {
    name = "cve-2016-4977"
    namespace = kubernetes_namespace_v1.vulnerables.metadata[0].name
  }

  spec {
    container {
      image = "${azurerm_container_registry.main.login_server}/vulnerables/cve-2016-4977:latest"
      name  = "demo"
      command = [ "tail", "-f", "/dev/null" ]
    }
  }

  depends_on = [
    azapi_resource_action.cve-2016-4977
  ]
}

resource "kubernetes_pod_v1" "cve-2016-7434" {
  metadata {
    name = "cve-2016-7434"
    namespace = kubernetes_namespace_v1.vulnerables.metadata[0].name
  }

  spec {
    container {
      image = "${azurerm_container_registry.main.login_server}/vulnerables/cve-2016-7434:latest"
      name  = "demo"
      command = [ "tail", "-f", "/dev/null" ]
    }
  }

  depends_on = [
    azapi_resource_action.cve-2016-7434
  ]
}