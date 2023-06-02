resource "helm_release" "books" {
  name      = "books"
  chart     = "../charts/books"
  namespace = "demo"

  depends_on = [helm_release.cluster_config]
}

resource "helm_release" "cluster_config" {
  name  = "cluster-config"
  chart = "../charts/cluster_config"
}
