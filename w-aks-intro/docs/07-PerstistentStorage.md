# Lab 7 - Using shared persistent storage for static content
In this lab we will fix one problem with our web - its logo is part of container image. We are lucky it is very small, but what if we need to access video files from multiple replicas?

Best approach would be to not access any static content via web layer at all - use Azure Blob Storage together with Azure CDN or Azure FrontDoor so content is serverd directly, not via your web server. But sometimes you need to have shared storage for your replicas to support traditional applications or share some state.

Topic of stateful applications is broad and very hard. Prefer to NOT run state in Kubernetes, because complexity is significant, and use platform services offered by Azure (like we did with database) or if you have to prefer shared-nothing architecture. Nevertheless in our case it makes sense to use shared storage for static content of our application. Goal is to change logo to demonstrate it does not have to be part of Docker image.

Make sure prefix is still configured in your terminal (bash):

```bash
export prefix="tomaskubica8"
```

If you use powershell:

```powershell
$prefix="tomaskubica8"
```

First we need to create storage account in Azure, file share and upload new logo file.

```bash
# Create storage account
az storage account create -n ${prefix}storage1 -g $prefix-rg

# Get storage key and create share - in bash 
export STORAGE_KEY=$(az storage account keys list -n ${prefix}storage1 -g $prefix-rg --query [0].value -o tsv)

# Get storage key and create share - in powershell
$STORAGE_KEY=$(az storage account keys list -n ${prefix}storage1 -g $prefix-rg --query [0].value -o tsv)

# Create file share
az storage share create -n images --account-name ${prefix}storage1 --account-key $STORAGE_KEY

# Upload image
cd resources/images
az storage file upload -s images --source ./ms.jpg --account-name ${prefix}storage1 --account-key $STORAGE_KEY
```

You can see files in Azure portal.

We will work on our test instance. Create secret with connection details to storage account.

```bash
# In bash
kubectl create secret generic images-secret \
    --from-literal=azurestorageaccountname=${prefix}storage1 \
    --from-literal=azurestorageaccountkey=$STORAGE_KEY \
    --namespace test

# In powershell
kubectl create secret generic images-secret `
    --from-literal=azurestorageaccountname=${prefix}storage1 `
    --from-literal=azurestorageaccountkey=$STORAGE_KEY `
    --namespace test
```

Modify web-deployment.yaml to reference Azure Files as Volume and map it to path in container file system. Add this into containers (eg. same level as image, env or ports):

```yaml
        volumeMounts:
          - name: myimages
            mountPath: /opt/bitnami/nginx/html/images
```

Path is where our application expects static content. We need to add myimages Volume to web-deployment.yaml so add this into spec (eg. same level as containers):

```yaml
      volumes:
        - name: myimages
          azureFile:
            secretName: images-secret
            shareName: images
            readOnly: true
```

Deploy changes and check whether logo has changed (note you might need to clear cache of your browser - or use Developer tools and network page, where you can disable caching for single window ). If yes, you have successfuly enabled external shared storage for your app.

Note there are much more capabilities in Azure Kubernetes Service for storage including disks of various speeds, Azure Files, Azure NetApp Files etc.