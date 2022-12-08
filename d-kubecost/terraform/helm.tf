resource "helm_release" "opencost" {
  provider = helm.helmaks1
  name     = "opencost"
  chart    = "../helm/opencost"
}

resource "helm_release" "demo" {
  provider = helm.helmaks1
  name     = "demo"
  chart    = "../helm/demo"

  set {
    name  = "L1"
    value = "A"
  }
}

resource "helm_release" "prometheus" {
  provider         = helm.helmaks1
  name             = "prometheus"
  chart            = "prometheus"
  repository       = "https://prometheus-community.github.io/helm-charts"
  namespace        = "prometheus"
  create_namespace = true

  set {
    name  = "extraScrapeConfigs"
    value = <<EOF
- job_name: opencost
  honor_labels: true
  scrape_interval: 1m
  scrape_timeout: 10s
  metrics_path: /metrics
  scheme: http
  dns_sd_configs:
  - names:
    - opencost.opencost
    type: 'A'
    port: 9003
EOF
  }

  set {
    name  = "pushgateway.enabled"
    value = "false"
  }

  set {
    name  = "alertmanager.enabled"
    value = "false"
  }
}

resource "helm_release" "grafana" {
  provider         = helm.helmaks1
  name             = "grafana"
  chart            = "grafana"
  repository       = "https://grafana.github.io/helm-charts"
  namespace        = "grafana"
  create_namespace = true

  set {
    name  = "service.type"
    value = "LoadBalancer"
  }
}
