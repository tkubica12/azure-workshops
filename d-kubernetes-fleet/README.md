# Azure Kubernetes Fleet demonstration

1. Deploy infrastructure using Terraform. 

```bash
cd terraform
terraform apply -auto-approve
```

2. Demonstrate AKS clusters are in default state with no applications or custom platform services deployed
   
3. Get credentials to fleet cluster

```bash
az fleet get-credentials -n d-kubernetes-fleet -g d-kubernetes-fleet
```

4. Deploy cluster resources

```bash
cd ../kubernetes
kubectl apply -k .
```