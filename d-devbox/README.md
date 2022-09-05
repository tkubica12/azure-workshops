# Microsoft Dev Box demo


```bash
cd bicep
az group create -n mydevcenter -l westeurope
az bicep build -f main.bicep && az deployment group create -g mydevcenter -f main.json
```

```bash
az group delete -n mydevcenter -y --no-wait
```
