# Lab 7 - Using persistent storage

Note - **running stateful apps is hard**. Do not do it unless you really have to, rather use platform services for state. Here is decision tree you can use for stateful apps in AKS: [https://tkubica12.github.io/cloud-storage-tests/aks-storage-decision-tree.html](https://tkubica12.github.io/cloud-storage-tests/aks-storage-decision-tree.html)

## Shared persistent storage for static content
In this lab we will fix one problem with our web - its logo is part of container image. We are lucky it is very small, but what if we need to access video files from multiple replicas?

**Best approach would be to not access any static content via web layer at all** - use Azure Blob Storage together with Azure CDN or Azure FrontDoor so content is serverd directly, not via your web server. But sometimes you need to have shared storage for your replicas to support traditional applications or share some state.

Topic of stateful applications is broad and very hard. **Prefer to NOT run state in Kubernetes**, because complexity is significant, and use platform services offered by Azure (like we did with database for our app) or if you have to than **prefer shared-nothing architecture**. Nevertheless in our case it makes sense to use shared storage for static content of our application. Goal is to change logo to demonstrate it does not have to be part of Docker image (it certainly should not - consider static content can include huge video files).

Make sure prefix is still configured in your terminal (bash):

```bash
export prefix="tomaskubica8"
```

If you use powershell:

```powershell
$prefix="tomaskubica8"
```

First we need to create storage account in Azure, file share and upload new logo file. We will use shared file storage that is spread across different availability zones so we get very high availability and can attach this storage from Pod running on Node in any AZ (note your cluster currently spreads AZs already).

```bash
# Create storage account
az storage account create -n ${prefix}storage1 -g $prefix-rg --sku Standard_ZRS

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

Deploy changes and check whether logo has changed (note you might need to clear cache of your browser - or use Developer tools and network page, where you can disable caching for single window ). If yes, you have successfully enabled external shared storage for your app.

Note there are much more capabilities in Azure Kubernetes Service for storage including disks of various speeds, Azure Files, Azure NetApp Files etc.

## Using Azure Disk
Next example is not using our existing application. We will create disks - one fast single-zone disk (LRS) and one multi-zone redundant disk (ZRS - logically slower on writes as it uses synchronous replica between AZs). Then we run 2 pods mounting first or second disk with preference to run in AZ 1 (so we can later simulate zone failure and see what happens easily).

Deploy storage example. Note we will use built-in storage class for LRS disk and configure our own for ZRS as no default is currently present in AKS.

```bash
cd kubernetes
kubectl apply -f disk-lrs.yaml
kubectl apply -f disk-zrs.yaml
```

We should see disks are created (all in zone 1 as you can check in MC_... resource group in portal) and both Pods running.

```bash
kubectl get pvc
kubectl get pv
kubectl get pods -o wide -l demo=disks
```

No simulate AZ failure by drain (basically shut down) all nodes in AZ 1.

```bash
kubectl drain aks-nodepool1-80146464-vmss000000 --delete-emptydir-data --ignore-daemonsets    # Change with your node name
```

After some time you should see ZRS based Pod to recover in different zone (on our other node in AZ 2) while LRS stays down in Pending state (until some node in AZ 1 show up - in other words until AZ 1 is up again).

```bash
kubectl get pods -o wide -l demo=disks
```

For singleton you should use ZRS disk or Azure Files ZRS in order to achieve zone redundancy. Note write latency will always be higher in such scenario. For trully stateful high performance applications running in AKS you must use shared-nothing architecture -> having multiple replicas accross zones each with its own fast (Premium, Premium v2 or even Ultra SSD) storage and data replication on software level (examples capable of this includes Kafka, Elastic, Redis, MS SQL, MongoDB, Cassandra...pretty much every modern SQL and noSQL database or messaging platform).

Uncordone node now.

```bash
kubectl uncordon aks-nodepool1-80146464-vmss000000    # Change with your node name
```

# Optional challenge - shared-nothing architecture with Azure Disks and StatefulSets
Note Deployments are not designed for stateful workloads that use separate storage for each replica. If you increase number of replicas in your Deployment this will lead to multiple Pods trying to write to the same disk and cause error.

In Kubernetes there is concept of StatefulSet for exactly those scenarios such as Kafka, Elastic, Cassandra or MongoDB. As optional task prepare StatefulSet that will automatically 3 instances across availability zones with each Pod having its own storage in respective zone. Check documentation here: [https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)