# AKS with Kata containers
In standard Kubernetes deployment containers share kernel which might not be considered enough isolation in dinance, healtcare or when running untrusted code in SaaS platform (eg. when SaaS customers can bring their own code to bring custom behavior - eg. custom data processing capabilities).

This demo deploy AKS with Mariner OS and enable Kata containers runtime - isolation using nested virtualization (hypervisor). Such solution enables hard multi-tenancy on shared AKS nodes. 


In kubernetes folder there are few examples to test.

```bash
# Get cluster credentials
az aks get-credentials -n d-aks-kata -g d-aks-kata --overwrite-existing --admin

# Deploy
kubectl apply -k kubernetes
```

How to get nested VM details from node:

```bash
# Get privileged access to node (in this case using node-shell extension)
kubectl node-shell yournodename

# Get cloud-hypervisor process
ps aux | grep cloud-hypervisor   # You will see one process per managed VM and you can see its management api socket

: '
root       68030  109  3.4 2979364 2231780 ?     Sl   07:13   3:16 /usr/bin/cloud-hypervisor --api-socket /run/vc/vm/7dbb721413c9c92bf218ba4387b5209c7127e390485b1cdaa9a6a026448bfd91/clh-api.sock
root       71273  316  4.0 3575380 2627176 ?     Sl   07:16   0:44 /usr/bin/cloud-hypervisor --api-socket /run/vc/vm/16dd8e263fabe20e723608ae701024affc07e05add8199d03aaba9938c042c17/clh-api.sock
'

# Get VM info
ch-remote --api-socket /run/vc/vm/7dbb721413c9c92bf218ba4387b5209c7127e390485b1cdaa9a6a026448bfd91/clh-api.sock info   
```