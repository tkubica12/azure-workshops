# Using ARM64 CPUs in Azure with AKS, Terraform, GitHub Actions and multi-arch images in ACR
GitHub actions in .github/workflows/aks-arm64-create.yml do the following>
- Login to Azure using federated identity (OIDC via AAD)
- Setup QEMU a build environment for multi architecture
- Setup Terraform and deploy ACR and AKS with AMD64 and ARM64 nodepools
- Build multi-arch and single-arch containers and posh to ACR
- Deploy Kubernetes objects to cluster using Kustomize

Check running containers - here I demonstrate how mutli-arch image can run on all nodes, but amd64 needs to be bounded only to amd64 architecture. Failing to do so results in errors. Two way to deal with running single-arch images on multi-arch cluster is either to use node affinity where needed (my case) or use taints (eg. by default arm64 node is not considered unless app explicitely tolerates that).

```
kubectl get pods -o wide
NAME                                      READY   STATUS             RESTARTS        AGE   IP            NODE                            NOMINATED NODE   READINESS GATES
app-amd64-85b69db494-8htjb                0/1     CrashLoopBackOff   7 (4m41s ago)   15m   10.244.1.6    aks-arm64-30808820-vmss000000   <none>           <none>
app-amd64-85b69db494-8jbll                1/1     Running            0               15m   10.244.0.21   aks-amd64-39196772-vmss000000   <none>           <none>
app-amd64-85b69db494-n7khv                0/1     CrashLoopBackOff   7 (4m51s ago)   15m   10.244.1.10   aks-arm64-30808820-vmss000000   <none>           <none>
app-amd64-85b69db494-xbrh7                1/1     Running            0               15m   10.244.0.15   aks-amd64-39196772-vmss000000   <none>           <none>
app-amd64-nodeaffinity-6664b98cf6-cz9mz   1/1     Running            0               15m   10.244.0.16   aks-amd64-39196772-vmss000000   <none>           <none>
app-amd64-nodeaffinity-6664b98cf6-dflnm   1/1     Running            0               15m   10.244.0.19   aks-amd64-39196772-vmss000000   <none>           <none>
app-amd64-nodeaffinity-6664b98cf6-nrq8t   1/1     Running            0               15m   10.244.0.17   aks-amd64-39196772-vmss000000   <none>           <none>
app-amd64-nodeaffinity-6664b98cf6-tgkns   1/1     Running            0               15m   10.244.0.18   aks-amd64-39196772-vmss000000   <none>           <none>
app-multi-579746c945-2zkbf                1/1     Running            0               15m   10.244.1.7    aks-arm64-30808820-vmss000000   <none>           <none>
app-multi-579746c945-8v8lz                1/1     Running            0               15m   10.244.1.8    aks-arm64-30808820-vmss000000   <none>           <none>
app-multi-579746c945-f4z45                1/1     Running            0               15m   10.244.0.20   aks-amd64-39196772-vmss000000   <none>           <none>
app-multi-579746c945-twd9b                1/1     Running            0               15m   10.244.1.9    aks-arm64-30808820-vmss000000   <none>           <none>
```



