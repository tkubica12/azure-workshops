resource "helm_release" "demo" {
  name  = "demo"
  chart = "../helm/demo"
}

resource "helm_release" "chaos_mesh" {
  name             = "chaos-mesh"
  chart            = "chaos-mesh"
  repository       = "https://charts.chaos-mesh.org"
  namespace        = "chaos-mesh"
  create_namespace = true

  set {
    name  = "dashboard.service.type"
    value = "LoadBalancer"
  }
  
  set {
    name  = "dashboard.env.LISTEN_PORT"
    value = "80"
  }

  set {
    name  = "chaosDaemon.runtime"
    value = "containerd"
  }

  set {
    name  = "chaosDaemon.socketPath"
    value = "/run/containerd/containerd.sock"
  }
}
