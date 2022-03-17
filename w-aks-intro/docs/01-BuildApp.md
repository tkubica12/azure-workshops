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
# Go to myappspa folder
cd resources/src/web

# Build v1 of myappspa
echo v1 > ./version
az acr build --registry $prefix --image web:v1 .

# Build v2 of myappspa (there is no real difference in code, just new text)
echo v2 > ./version
az acr build --registry $prefix --image web:v2 .

# Go to myappspa folder
cd ../api

# Build backend microservice
az acr build --registry $prefix --image api:v1 .
```


