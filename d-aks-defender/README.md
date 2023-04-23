# Microsoft Defender for containers
Deploy demo environment and get credentials

```bash
cd terraform
terraform init
terraform apply -auto-approve

az aks get-credentials -n d-aks-defender -g d-aks-defender --admin --overwrite-existing
```

## Runtime security
Deploy demo (cron jobs executing every 10 minutes) doing suspicious things inside containers that runtime security should detect.

```bash
kubectl apply -k ./kubernetes_runtime
```

See alerts in Microsoft Defender.

## Kubernetes API security
Deploy demo doing suspicious things on Kubernetes API layer.

```bash
kubectl apply -k ./kubernetes_api
```

See alerts in Microsoft Defender.

## Image security
Azure Container Registry contains vulnerable image - check in ACR -> Microsoft Defender for Cloud, click on recommendations. 

## Cluster recommendations
See recommendations on AKS -> Microsoft Defender for Cloud

## Policies
Deploy demo that violates policies.

```bash
kubectl apply -k ./kubernetes_policy
```