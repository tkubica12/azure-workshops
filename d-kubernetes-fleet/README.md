# Azure Kubernetes Fleet demonstration

1. Deploy infrastructure using Terraform. 

```bash
cd terraform
terraform apply -auto-approve
```

2. Demonstrate AKS clusters are in default state with no applications or custom platform services deployed
   
3. Get credentials to fleet cluster

```bash
az fleet get-credentials -n d-kubernetes-fleet -g d-kubernetes-fleet --overwrite
```

4. Deploy cluster resources

```bash
cd ../kubernetes
kubectl apply -k .
```

5. Demonstrate resources gets quickly deployed to all clusters

6. Find external service IP and demonstrate global balancing of north-south traffic. 

```bash
while true; do time -p curl http://20.23.180.148/info; echo; echo; sleep 1; done 
```