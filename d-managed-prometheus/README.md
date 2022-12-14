# Azure Managed Prometheus with Azure Managed Grafana
This repo contains demonstration of managed Prometheus and Grafana in Azure.

Terraform is used to provision complete environment automatically. Because quite a few preview features are used, AzApi Terraform provider is used for some of objects.

Solution creates:
- Azure Managed Grafana
- Azure Managed Prometheus using Azure Monitor Workspace
- Azure Kubernetes Service enrolled for monitoring
- Simple application deployed to AKS demonstrating scraping custom prometheus metrics

Deploynent:
1. Deploy infrastructure in terraform folder using 
   ```
   terraform apply
   ``` 
2. Get cluster credentials with 
   ```
   az aks get-credentials -n d-managed-prometheus -g d-managed-prometheus --admin --overwrite-existing
   ```
3. Deploy application in kubernetes folder with 
   ```
   kubectl apply -f .
   ``` 
4. To demonstrate remote-write capability, get credentials to second cluster
   ```
   az aks get-credentials -n d-prometheus-remotewrite -g d-managed-prometheus --admin --overwrite-existing
   ```
5. Get Azure Metrics workspace Metrics ingestion endpoint in main resource group
6. Get Client ID for AKS kubelet identity used as client for remote write
   ```
   az identity show -n d-prometheus-remotewrite-agentpool -g MC_d-managed-prometheus_d-prometheus-remotewrite_westeurope --query clientId -o tsv
   ```
7. Update file remote-write/values.yaml with workspace URL and client ID
8. Deploy Prometheus with sidecar providing remote-write to Azure Monitor for Prometheus
   ```
   cd remote-write
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   helm upgrade -i -f values.yaml prometheus prometheus-community/kube-prometheus-stack
   ```

To demonstrate:
- Open Grafana and show built-in dashboards for nodes, workloads, pods etc.
- Go to Explore section and search fo my_failure metrics (custom metrics from our app) and demonstrate how you can build custom view of custom metric

