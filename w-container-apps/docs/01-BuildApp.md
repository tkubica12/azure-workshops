# Build application container and try to run it
In this lab you will look at provided application and build it.

Store yourname and some random number as variable.

If you use bash:

```bash
export prefix="tomaskubica8"
```

If you use powershell:

```powershell
$prefix="tomaskubica8"
```


Create Resource Group

```bash
az group create -n $prefix-rg -l northeurope
```

Create Azure Container Registry

```bash
az acr create -n $prefix -g $prefix-rg --sku Basic --admin-enabled
```

Build containers directly in repository

```bash
# Build backend microservice
cd w-container-apps/resources/src/api
az acr build --registry $prefix --image api:v1 .

# Build event generator
cd ../event-generator
az acr build --registry $prefix --image event-generator:v1 .

# Build event processor
cd ../event-processor
az acr build --registry $prefix --image event-processor:v1 .

# Import todo web app from public registry to your private registry
az acr import -n $prefix --source ghcr.io/tkubica12/todo-web:v1 --image web:v1
az acr import -n $prefix --source ghcr.io/tkubica12/todo-web:v2 --image web:v2
```


