# Kubernetes Operators demo on AKS
This folder contains demo of Kubernetes Operators for customer talk. In this README you will find how to reproduce.

**See [markmap](https://tkubica12.github.io/azure-workshops/kubernetes-operators.html) that will be used during lecture**

## Building resources

```bash
# Go to terraform folder
cd terraform

# Export variables (service prinicpal logins and password)
export TF_VAR_AZURE_SUBSCRIPTION_ID=yoursubscriptionid
export TF_VAR_AZURE_TENANT_ID=yourtenantid
export TF_VAR_AZURE_CLIENT_ID=yourclientid
export TF_VAR_AZURE_CLIENT_SECRET=yourclientsecret
export TF_VAR_password=passwordforcreatedresources

# Deploy
terraform init
terraform plan
terraform apply -auto-approve

# Get credentials
az aks get-credentials -g operators-demo-aks -n operators-demo-aks --admin --overwrite-existing

# Clean up after demo
terraform destroy -auto-approve
az group delete -n demo-aso-rg -y
```

## How to demo

### ReplicaSet
1. Show definition and number of replicas
2. Delete Pod and see ReplicaSet fixing this
3. Do live edit of pod and change label
4. Change label back

### AKS GitOps with Flux v2
1. Explain CRDs such as GitRepo, HelmRepo, HelmRelease or Kustomization
2. Show controllers - helm, kustomize, source, notification
3. Explain Git repo structure - Kustomize and Helm
4. Change ReplicatSet nuber of replicas and commit
5. Show how state gets synchronize and Pods created

## Arc for Data Services - Azure SQL operator
1. Show running SQL and CRD (sqlmanagedinstance in arc namespace)
2. Create new database definition and commit
3. In meantime show PVs, PVCs, StatefulSets and other components
4. See another SQL instance being created
5. You may check Kibana and Grafana in cluster (check services for IPs and ports)

### Azure Service Operator
1. Show CRD FlexibleServer and ResourceGroup
2. Show this database in Azure
3. Change sizing to Standard_B2s or Standard_B1ms and commit the change
4. Demonstrate change gets reflected on Azure resource

### Argo Rollouts
1. Access testing page at tomaskubicaoperatordemo123.northeurope.cloudapp.azure.com 
2. Change rollout yaml to tag green or red

### KEDA
1. Desribed ScaledObject.
2. Show pods in keda namespace.
3. In Azure Portal generate new message in Service Bus and see Pods comming up.

### DAPR
TBD