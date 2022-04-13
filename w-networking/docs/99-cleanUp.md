```bash
# Configure prefix (in bash)
export prefix=tomaskubica4

# Configure prefix (in PowerShell)
$prefix="tomaskubica4"

# Delete resource groups
az group delete -n $prefix-project1 -y
az group delete -n $prefix-project2 -y
az group delete -n $prefix-onprem -y
az group delete -n $prefix-dmz -y
az group delete -n $prefix-shared -y
az group delete -n $prefix-central -y

```