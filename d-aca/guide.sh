# Create Resource Group
az group create -n aca -l westeurope

# Create Azure Container App Environment
az containerapp env create -n aca-env -g aca -l westeurope

# Create scheduled job
az containerapp job create \
    -n demojob \
    -g aca \
    --environment aca-env \
    --trigger-type "Schedule" \
    --replica-timeout 600 \
    --replica-retry-limit 5 \
    --replica-completion-count 1 \
    --parallelism 1 \
    --image "mcr.microsoft.com/k8se/quickstart-jobs:latest" \
    --cpu "0.25" --memory "0.5Gi" \
    --cron-expression "*/2 * * * *"

# Deploy web application
az containerapp up \
    -n demoweb \
    -g aca \
    --environment aca-env \
    --image mcr.microsoft.com/azuredocs/containerapps-helloworld:latest \
    --target-port 80 \
    --ingress external

# Custom FQDN with free certificate
export native_fqdn=$(az containerapp show -n demoweb -g aca -o tsv --query "properties.configuration.ingress.fqdn")
export domain_verification=$(az containerapp show -n demoweb -g aca -o tsv -o tsv --query "properties.customDomainVerificationId")
az network dns record-set cname set-record -n web -g base -z demo.tkubica.biz -c $native_fqdn
az network dns record-set txt add-record -n asuid.web -g base -z demo.tkubica.biz -v $domain_verification
az containerapp hostname add --hostname web.demo.tkubica.biz -g aca -n demoweb
az containerapp hostname bind --hostname web.demo.tkubica.biz -g aca -n demoweb --environment aca-env --validation-method CNAME

# Destroy resources
az network dns record-set cname delete -n web -g base -z demo.tkubica.biz -y
az network dns record-set txt delete -n asuid.web -g base -z demo.tkubica.biz -y
az group delete -n aca -y