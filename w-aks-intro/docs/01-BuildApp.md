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

Build api container directly in repository

```bash
# Go to myappspa folder
cd resources/src/web

# Build backend microservice
az acr build --registry $prefix --image api:v1 .
```

Import web containers from Docker Hub to your repository.

```bash
az acr import -n $prefix --source ghcr.io/tkubica12/todo-web:v1 --image web:v1
az acr import -n $prefix --source ghcr.io/tkubica12/todo-web:v2 --image web:v2
```

