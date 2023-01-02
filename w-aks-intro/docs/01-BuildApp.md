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

# Optional challenge - build PHP app
In this optional task you need to build and run simple PHP application that you find in folder resources/src/php. Consider [https://hub.docker.com/_/php](https://hub.docker.com/_/php) in variant with apache as your base image and prepare your Dockerfile.

Build it using in php folder

```
az acr build --registry $prefix --image php:v1 .
```

Run it using Azure Container Instance

```
az container create -g $prefix-rg -n php --image $prefix.azurecr.io/php:v1 --cpu 1 --memory 1 --registry-login-server $prefix.azurecr.io --registry-username $prefix --registry-password $(az acr credential show -n $prefix --query passwords[0].value -o tsv) --ip-address Public
```

Using UI find public IP and test your application is working.

Delete container instance

```
az container delete -g $prefix-rg -n php -y
```