# Azure Chaos Studio demo

Deploy infrastructure

```bash
az group create -n chaos -l westeurope
az bicep build -f bicep/main.bicep 
az deployment group create -g chaos -n chaos-infrastructure --template-file bicep/main.json
```

# Experiments

## VM shutdown experiment
Run experiment and watch different VMs getting stopped.

## VM Fault injection experiment
This experiment consists of few faults injected.

Monitor network latency from Windows VM 1

```bash
az serial-console connect -n windowsVm1 -g chaos
cmd
ch -si 1
powershell
(Measure-Command -Expression { Invoke-WebRequest -Uri linuxVm2 -UseBasicParsing }).TotalMilliseconds
```

In portal check CPU usage of Windows VM 2.

In portal check number of IO Write operations on Linux VM1 operating system disk.

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
