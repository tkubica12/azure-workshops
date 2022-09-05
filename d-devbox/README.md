# Microsoft Dev Box demo
Build demo environment for Dev Box including Dev Center, Project, Network, Network connection, two Dev Pools and RBAC for one developer.

Deploy infrastructure.

```bash
cd bicep
az group create -n mydevcenter -l westeurope
export DEV_OBJECT_ID=$(az ad user show --id $(az account show --query user.name -o tsv) --query objectId -o tsv)
az bicep build -f main.bicep && az deployment group create -g mydevcenter -f main.json --parameters dev_object_id=$DEV_OBJECT_ID
```

Access dev box portal at [https://devbox.microsoft.com/](https://devbox.microsoft.com/)

To destroy demo environment simply delete resource group.

```bash
az group delete -n mydevcenter -y --no-wait
```
