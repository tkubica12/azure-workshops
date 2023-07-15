# resource "helm_release" "bootstrap" {
#   name      = "demo"
#   chart     = "../charts/bootstrap"
#   namespace = "argocd"

#   depends_on = [helm_release.argocd]
# }

# resource "helm_release" "argocd" {
#   name             = "argocd"
#   chart            = "https://github.com/argoproj/argo-helm/releases/download/argo-cd-5.29.1/argo-cd-5.29.1.tgz"
#   namespace        = "argocd"
#   create_namespace = true

#   set {
#     name  = "server.service.type"
#     value = "LoadBalancer"
#   }
# }

# resource "helm_release" "bootstrap2" {
#   provider = helm.aks2
#   name      = "demo"
#   chart     = "../charts/bootstrap"
#   namespace = "argocd"

#   depends_on = [helm_release.argocd2]
# }

# resource "helm_release" "argocd2" {
#   provider = helm.aks2
#   name             = "argocd"
#   chart            = "https://github.com/argoproj/argo-helm/releases/download/argo-cd-5.29.1/argo-cd-5.29.1.tgz"
#   namespace        = "argocd"
#   create_namespace = true

#   set {
#     name  = "server.service.type"
#     value = "LoadBalancer"
#   }
# }
