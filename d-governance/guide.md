```bash
# Create new resource group
az group create -n governance-testing -l swedencentral
az network public-ip create -g governance-testing -n test-ip

# Try creating RBAC assignment on sub and rg level

# NOT OK
az role assignment create --assignee user@tkubica.biz \
    --role Owner \
    --scope /subscriptions/$(az account show --query id -o tsv)

# OK
az role assignment create --assignee user@tkubica.biz \
    --role Contributor \
    --scope /subscriptions/$(az account show --query id -o tsv)

# OK
az role assignment create --assignee user@tkubica.biz \
    --role Owner \
    --scope $(az group show -n governance-testing --query id -o tsv)

# OK
az role assignment create --assignee user@tkubica.biz \
    --role Owner \
    --scope $(az network public-ip show -g governance-testing -n test-ip --query id -o tsv)

# Delete RBAC assignment on sub and rg level
az role assignment delete --assignee user@tkubica.biz \
    --role Owner \
    --scope /subscriptions/$(az account show --query id -o tsv)

az role assignment delete --assignee user@tkubica.biz \
    --role Contributor \
    --scope /subscriptions/$(az account show --query id -o tsv)

az role assignment delete --assignee user@tkubica.biz \
    --role Owner \
    --scope $(az group show -n governance-testing --query id -o tsv)

az role assignment delete --assignee user@tkubica.biz \
    --role Owner \
    --scope $(az network public-ip show -g governance-testing -n test-ip --query id -o tsv)

az group delete -n governance-testing -y --no-wait
```