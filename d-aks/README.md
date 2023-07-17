# AKS demo
To get credentials:

```bash
az aks get-credentials -n d-aks -g d-aks --overwrite-existing --admin
```

**GitOps demo**- change d-aks/kubernetes/charts/myapp/templates and increase number of replicas. Showcase it gets pulled by both AKS clusters.

```mermaid
graph LR;
flux_entrypoint --> cluster_layer([Cluster kustomize layer])
cluster_layer -- patches ---> base_layer_infra([Infra kustomize layer])
cluster_layer -- patches ---> base_layer_apps([Apps kustomize layer])
base_layer_infra -- patches --> argo_rollouts([Argo rollouts controller])
argo_rollouts -- patches --> argo_rollouts_resources[/Resources: controller, service, .../]
base_layer_infra -- patches --> namespaces[/Resource: namespaces/]
base_layer_infra -- input variables --> cert_manager[[Helm: cert-manager]]
base_layer_infra -- input variables --> nginx_ingress[[Helm: nginx-ingress]]
base_layer_apps -- input variables --> canary_demo[[Helm: canary-demo]]
base_layer_apps -- input variables --> myapp[[Helm: myapp]]

myapp --> deployment_myapp[/Resource: deployment/]
myapp --> service_myapp[/Resource: service/]
myapp --> ingress_myapp[/Resource: ingress/]

canary_demo --> ingress_canary_demo[/Resource: ingress/]
canary_demo --> service_canary_demo[/Resource: service/]
canary_demo --> preview_service_canary_demo[/Resource: preview_service/]
canary_demo --> rollout_canary_demo[/Resource: rollout/]

nginx_ingress --> deployment_nginx_ingress[/Resource: deployment/]
nginx_ingress --> service_nginx_ingress[/Resource: service/]
nginx_ingress --> other_nginx_ingress[/Resource: other resources/]

cert_manager --> deployment_cert_manager[/Resource: deployment/]
cert_manager --> service_cert_manager[/Resource: service/]
cert_manager --> other_cert_manager[/Resource: other resources/]
```


**Argo Rollouts demo** - modify d-aks/charts/canary_demo/templates/canary-rollout.yaml image tag to different color (gree, blue, red). Showcase how:
- On ingress IP demo app is showing 5% of boxes with new color
- ArgoCD UI shows paused deployment
- Argo Rollouts UI shows 5% and waits for input
- Show Ingress configuration for canary
- In Argo Rollout UI advance deployment and see how new version is rolled out gradually
- Discus how metrics can be used to decide whether advance or rollback



