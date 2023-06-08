# ChaosMesh on AKS
This is demo of open source project ChaosMesh on AKS. For broader view on Chaos engineering see demo with Azure Chaos Studio [here](../d-chaos-studio/README.md).

To access dashboard you need to create token

```bash
az aks get-credentials -n d-aks-chaosmesh -g d-aks-chaosmesh --admin --overwrite-existing
kubectl create token chaosdashboard
```

Use UI to run experiments:

## Pod killer
Configure pod killer of app:myapp1

## Network delay
From client container run 

```bash
while true; do time curl -I myapp1; sleep 1; done
```

Configure experiment to add delay.

## CPU stress
Generate CPU load and show in k9s metrics