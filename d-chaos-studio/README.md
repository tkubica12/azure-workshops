# Azure Chaos Studio demo
This demonstration focus on chaos engineering with Azure Chaos Studio.

Deploy infrastructure with all neccessary configurations, VMs, Kubernetes cluster, chaos experiments etc.

```bash
az group create -n chaos -l westeurope
az bicep build -f bicep/main.bicep 
az deployment group create -g chaos -n chaos-infrastructure --template-file bicep/main.json
```

After deployment you might need to wait few minutes for AKS GitOps to deploy chaos mesh and application demos.

# Experiments
Here are experiments that are part of this demonstration.

## VM shutdown experiment
Run experiment and watch different VMs getting stopped.

## VM Fault injection experiment
This experiment consists of few faults injected.

Monitor network latency from Windows VM 1. During experiment you should see much bigger latency.

```bash
az serial-console connect -n windowsVm1 -g chaos
cmd
ch -si 1
powershell
(Measure-Command -Expression { Invoke-WebRequest -Uri linuxVm2 -UseBasicParsing }).TotalMilliseconds
```

In portal check CPU usage of Windows VM 2 as it spikes during experiment (note Azure metrics might be delayed for few minutes as we are not using agent-based monitoring for simplicity).

In portal check number of IO Write operations on Linux VM1 operating system disk (note Azure metrics might be delayed for few minutes as we are not using agent-based monitoring for simplicity).

## Kubernetes experiments
Download credentials to access cluster.

```bash
az aks get-credentials -n mesh-demo-aks -g chaos
```

I suggest to use k9s UI to demonstrate effects of experiments.

### Pod experiments
Watch Pods in k9s. 

In first steps random Pods are killed roughly every 30 seconds.

In next steps fault is injected into Pod in myapp1 and myapp2 so it stops responding. Note myapp1 recognize this as liveness probe and readiness probe fails so Kubernetes keep restarting Pod and does not send traffic to it. myapp2 due to missing probes has not detected issue and we have user impact here.

You may also run continuos test from client Pod this way:

```bahs
kubectl exec -it -n client deployment/client -- bash -c "while true; do curl --connect-timeout 0.1 -I http://myapp1.default.svc.cluster.local; done"
kubectl exec -it -n client deployment/client -- bash -c "while true; do curl --connect-timeout 0.1 -I http://myapp2.default.svc.cluster.local; done"
```

### Stress experiments
Watch pods in k9s and observe one myapp1 pod experiencing higher CPU usage and one pod in myapp2 having high memory usage (you might OOM kills).

### Network experiments
Jump to myapp1 Pod before experiment:

```bash
kubectl exec -it deployment/myapp1 -- bash -c "time curl http://myapp2"  # delay will be short
kubectl exec -it deployment/myapp2 -- bash -c "curl http://myapp1"  # you will get default NGINX response
kubectl exec -it deployment/myapp1 -- bash -c "getent hosts tomaskubica.cz"  # you will get stable correct response
```

Run experiment that will add network latency, fake HTTP responses and fake random DNS response on tomaskubica.cz.

```bash
kubectl exec -it deployment/myapp1 -- bash -c "time curl http://myapp2"  # will take much longer
kubectl exec -it deployment/myapp2 -- bash -c "curl http://myapp1"  # fake JSON response
kubectl exec -it deployment/myapp1 -- bash -c "getent hosts tomaskubica.cz"  # random IPs with every call
```