resource "helm_release" "books" {
  name      = "books"
  chart     = "../charts/books"
  namespace = "demo"

  depends_on = [helm_release.namespaces]
}

resource "helm_release" "namespaces" {
  name  = "namespaces"
  chart = "../charts/namespaces"
}
