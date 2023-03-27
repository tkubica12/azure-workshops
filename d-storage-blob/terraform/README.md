# Azure Storage Blob demo
1. Open blob and see different RBAC on different containers
2. Access from container1 as identity1 and see you can write only to one container
```bash
az container exec -g d-storage-blob -n container1 --container-name container --exec-command "/bin/bash"
az login --identity
az storage account list -o table --query [].name
blobaccountname=$(az storage account list -o tsv --query [].name | grep blob)
filename=file$RANDOM
touch $filename
az storage blob upload -f $filename -c team1 -n $filename --account-name $blobaccountname --auth-mode login     # OK
az storage blob upload -f $filename -c team2 -n $filename --account-name $blobaccountname --auth-mode login     # No access
exit
```