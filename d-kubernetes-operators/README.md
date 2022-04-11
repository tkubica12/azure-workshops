# Kubernetes Operators demo on AKS
This folder contains demo of Kubernetes Operators for customer talk. In this README you will find how to reproduce.

**See [markmap](https://tkubica12.github.io/azure-workshops/kubernetes-operators.html) that will be used during lecture**

## Building resources

```bash
# Create AKS cluster and get credentials
az group create -n operators-demo-aks -l northeurope
az aks create -g operators-demo-aks -n operators-demo-aks -c 5 -x -s Standard_B4ms -y
az aks get-credentials -g operators-demo-aks -n operators-demo-aks --admin --overwrite-existing

# Configure GitOps operator
az k8s-configuration flux create -n operators-demo-aks \
  -g operators-demo-aks \
  -c operators-demo-aks \
  --namespace gitops-demo \
  -t managedClusters \
  --scope cluster \
  --sync-interval 30s \
  -u https://github.com/tkubica12/azure-workshops/
  --branch main \
  --kustomization name=platform path=./d-kubernetes-operators/platform prune=true sync_interval=120s retry_interval=120s force=true \
  --kustomization name=demo path=./d-kubernetes-operators/demo prune=true sync_interval=30s retry_interval=30s force=true

# Configure your envs with Service Principal and create secrets
# Note you might need to wait for namespaces to be available (just repeate if commend fails)
export subscription=yoursubscriptionid
export tenant=yourtenantid
export principal=yourclientid
export client_secret=yourclientsecret
export password=passwordforcreatedresources

cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: aso-controller-settings
  namespace: azureserviceoperator-system
stringData:
  AZURE_SUBSCRIPTION_ID: "$subscription"
  AZURE_TENANT_ID: "$tenant"
  AZURE_CLIENT_ID: "$principal"
  AZURE_CLIENT_SECRET: "$client_secret"
---
apiVersion: v1
kind: Secret
metadata:
  name: mysecrets
  namespace: default
stringData:
  password: $password
---
apiVersion: v1
kind: Secret
metadata:
  name: sql1-login-secret
  namespace: arc
stringData:
  username: labuser
  password: $password
---
apiVersion: v1
kind: Secret
metadata:
  name: metricsui-admin-secret
  namespace: arc
stringData:
  username: labuser
  password: $password
---
apiVersion: v1
kind: Secret
metadata:
  name: logsui-admin-secret
  namespace: arc
stringData:
  username: labuser
  password: $password
EOF

# Create storage account for KEDA demo and store secrets
az servicebus namespace create -n tomaskubicademo58882 -g operators-demo-aks --sku Basic
az servicebus queue create -n orders --namespace-name tomaskubicademo58882 -g operators-demo-aks

cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: sbkey
  namespace: default
stringData:
  servicebus-connectionstring: "$(az servicebus namespace authorization-rule keys list -n RootManageSharedAccessKey --namespace-name tomaskubicademo58882 -g operators-demo-aks --query primaryConnectionString -o tsv)"
EOF

# Clean up after demo
az group delete -n operators-demo-aks -y
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