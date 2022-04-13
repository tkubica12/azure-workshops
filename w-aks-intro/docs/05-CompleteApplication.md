# Lab 5 - Complete our application by adding api, database and ingress
In this lab we will create managed database in Azure, deploy api component in Kubernetes and configure credentials to access database.

Make sure your prefix is still in defined in your session.

If you use bash:

```bash
export prefix="tomaskubica8"
```

If you use powershell:

```powershell
$prefix="tomaskubica8"
```

Create Azure Database for PostgreSQL

```bash
# in bash

# Create Private DNS zone
az network private-dns zone create -g $prefix-rg -n psqllab.private.postgres.database.azure.com

# Associate Private DNS zone with your VNET
az network private-dns link vnet create --name psqldnslink \
    --registration-enabled false \
    -g $prefix-rg \
    --virtual-network $(az network vnet show -n $prefix-vnet -g $prefix-rg --query id -o tsv) \
    --zone-name psqllab.private.postgres.database.azure.com

az postgres flexible-server create --name $prefix-psql \
    -g $prefix-rg \
    --admin-user psqladmin \
    --admin-password Azure12345678! \
    --sku-name Standard_B1ms \
    --tier Burstable \
    --version 13 \
    --high-availability Disabled \
    --subnet $(az network vnet subnet show -g $prefix-rg --vnet-name $prefix-vnet -n db --query id -o tsv) \
    --private-dns-zone $(az network private-dns zone show -g $prefix-rg -n psqllab.private.postgres.database.azure.com --query id -o tsv)

az postgres flexible-server db create -g $prefix-rg  --server-name $prefix-psql --database-name todo
```

```powershell
# in PowerShell

# Create Private DNS zone
az network private-dns zone create -g $prefix-rg -n psqllab.private.postgres.database.azure.com

# Associate Private DNS zone with your VNET
az network private-dns link vnet create --name psqldnslink `
    --registration-enabled false `
    -g $prefix-rg `
    --virtual-network $(az network vnet show -n $prefix-vnet -g $prefix-rg --query id -o tsv) `
    --zone-name psqllab.private.postgres.database.azure.com

az postgres flexible-server create --name $prefix-psql `
    -g $prefix-rg `
    --admin-user psqladmin `
    --admin-password Azure12345678! `
    --sku-name Standard_B1ms `
    --tier Burstable `
    --version 13 `
    --high-availability Disabled `
    --subnet $(az network vnet subnet show -g $prefix-rg --vnet-name $prefix-vnet -n db --query id -o tsv) `
    --private-dns-zone $(az network private-dns zone show -g $prefix-rg -n psqllab.private.postgres.database.azure.com --query id -o tsv)

az postgres flexible-server db create -g $prefix-rg  --server-name $prefix-psql --database-name todo
```

We will now store connection string to our database in Kubernetes Secret (note storing in Azure Key Vault is much more secure, but for simplicity we will stick with Secret for now).

```bash
# Create Secret in Bash
kubectl create secret generic psql-secret --from-literal=postgresqlurl='jdbc:postgresql://'${prefix}'-psql.postgres.database.azure.com:5432/todo?user=psqladmin&password=Azure12345678!&ssl=true'

# Create Secret in PowerShell
kubectl create secret generic psql-secret --from-literal=postgresqlurl="jdbc:postgresql://${prefix}-psql.postgres.database.azure.com:5432/todo?user=psqladmin&password=Azure12345678!&ssl=true"
```

Deploy api application and service (make sure you modify image to match your registry). Also note we are using liveness probe (used for detection that application is alive) and readiness probe (used for balancers to understand whether application is ready to serve requests).

```bash
kubectl apply -f api-deployment.yaml
kubectl apply -f api-service.yaml
```

Watch application logs to make sure there are no errors.

```bash
# Get logs from api Pod
kubectl logs api-5548d8dc44-tm2wz

# You should see: My Spring Boot app started ...
```

Our web is Single Page Application (SPA) that runs Angular code in user browser which then access api component. Unlike traditional static web apps, which talk to backend from server, modern apps often access backend APIs from client. Therefore we need to make both web and api accessible from outside of cluster (in our case we will use public IP, but you can also use IP internal to VNET for internal users or for publication via your own DMZ). Also - to maintain security standards we want app to access only its own domain so we need to run both web and api under same domain, just different paths (in / there should be our web while on /api should be our api), This means using L7 balancer (reverse proxy) which is Kubernetes called Ingress (we will use Microsoft-managed ingress implementation).

First find out what is public IP of Azure Application Gateway component (managed ingress) for your cluster.

```bash
az network public-ip show -n applicationgateway-appgwpip -g MC_$prefix-rg_$prefix-aks_northeurope --query ipAddress -o tsv
```

In standard situation you will register this IP with your domain (A record). For simplicity we will now use nip.io service which provider DNS resolution service something.1.2.3.4.nip.io -> 1.2.3.4. Modify ingress.yaml to reflect your nip.io based hostname.

```bash
kubectl apply -f ingress.yaml
```

Open application in your browser. You should be able to add, edit and delete todo items. If not, troubleshoot.

Congratulations! Your app is running properly.