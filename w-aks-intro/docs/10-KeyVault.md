# Lab 10 - Using Azure Key Vault to manage secrets
While using Kubernetes Secrets objects is good start (and certainly way better than storing secrets in deployment files) it is typically not considered enterprise-grade. For it we will use specialized Azure Key Vault service and integrate it with Kubernetes.

Deploy Azure Key Vault

```bash
az keyvault create -n $prefix-kv -g $prefix-rg -l northeurope --enable-rbac-authorization
```

Grant read/write permissions to yourself

```bash
# In bash
az role assignment create --role "Key Vault Secrets Officer" \
    --assignee $(az account show --query user.name -o tsv) \
    --scope $(az keyvault show -n $prefix-kv -g $prefix-rg --query id -o tsv)

# In PowerShell
az role assignment create --role "Key Vault Secrets Officer" `
    --assignee $(az account show --query user.name -o tsv) `
    --scope $(az keyvault show -n $prefix-kv -g $prefix-rg --query id -o tsv)
```

Grant read permissions to AKS (secrets provider class)

```bash
# In bash
az role assignment create --role "Key Vault Secrets Officer" \
    --assignee $(az aks show -g $prefix-rg -n $prefix-aks --query addonProfiles.azureKeyvaultSecretsProvider.identity.clientId -o tsv) \
    --scope $(az keyvault show -n $prefix-kv -g $prefix-rg --query id -o tsv)

# In PowerShell
az role assignment create --role "Key Vault Secrets Officer" `
    --assignee $(az aks show -g $prefix-rg -n $prefix-aks --query addonProfiles.azureKeyvaultSecretsProvider.identity.clientId -o tsv) `
    --scope $(az keyvault show -n $prefix-kv -g $prefix-rg --query id -o tsv)
```

Create secret in Key Vault

```bash
# In Bash
az keyvault secret set -n postgresqlurl \
    --vault-name $prefix-kv \
    --value 'jdbc:postgresql://'${prefix}'-psql.postgres.database.azure.com:5432/todo?user=psqladmin&password=Azure12345678!&ssl=true'

# In PowerShell
az keyvault secret set -n postgresqlurl \
    --vault-name $prefix-kv \
    --value "jdbc:postgresql://${prefix}-psql.postgres.database.azure.com:5432/todo?user=psqladmin&password=Azure12345678!&ssl=true"
```

Create new namespace for new instance of our application using secrets provider class.

```bash
kubectl create namespace moresecure
```

Now we need to deploy Secrets Provider Class that can bring data from Azure Key Vault into Kubernetes. You will find it in file secrets-provider-class.yaml and you need to change few parameters - clientid for identity, tenantid and Key Vault name.

Note that Secrets Provider Class is used to map secrets as files into container as this is considered most secure option and allows for dynamic rotation if secret changes. But our legacy application does not support this and requires this to be in environmental variable. Therefore we will map it as file (this is always needed for Secrets Provider Class to work), but also synchronize to Kubernetes Secret so it can be passed as env to our application.

```yaml

```bash
kubectl apply -f secrets-provider-class.yaml -n moresecure
```

Let's deploy api component now. Look into logs to make sure it has correctly started so login to database does work.

```bash
kubectl apply -f api-deployment-kv.yaml -n moresecure
```

# Optional challenge - package our application for test and prod environments
Surely modifying YAML directly to put things like Key Vault name is not good practice as we will likely have different Key Vault for test and for production.

In lab 6 you have prepared parametrized solution to deploy application in different environments using Kustomize (or Helm in optional challenge). Modify your solution adding one Key Vault for test and one for production and make KV name as just parameter for different environments (using Kustomize overlay or Helm template parameter).