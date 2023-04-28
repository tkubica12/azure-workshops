resource "helm_release" "bootstrap" {
  name  = "demo"
  chart = "../charts/bootstrap"
}

resource "helm_release" "argocd" {
  name             = "argocd"
  chart            = "https://github.com/argoproj/argo-helm/releases/download/argo-cd-5.29.1/argo-cd-5.29.1.tgz"
  namespace        = "argocd"
  create_namespace = true

  set {
    name  = "server.service.type"
    value = "LoadBalancer"
  }
}
