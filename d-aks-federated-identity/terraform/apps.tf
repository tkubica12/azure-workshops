resource "kubernetes_pod" "main" {
  metadata {
    name = "client"

    annotations = {
      "azure.workload.identity/inject-proxy-sidecar" = "true"
      "azure.workload.identity/proxy-sidecar-port"   = "8080"
    }
  }

  spec {
    service_account_name = kubernetes_service_account.identity1.metadata[0].name

    container {
      image = "nginx:latest"
      name  = "client"
    }
  }
}
