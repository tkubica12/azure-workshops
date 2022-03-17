# Lab 3 - Object storage for applications, archiving and Big Data
In this lab we will play with object storage - modern and cheap way to store unstructured data. We will focus on basic usage, different performance tiers, data protection capabilities and integration with advanced search. No that this technology plays important role in Big Data systems with hierarchical namespace capability for Data Lake scenarios (beyond scope of this lab). 

## Basic concepts
In your storage account create new private container.

![](./images/L03-001.png)
![](./images/L03-002.png)

Upload some image. In Advance make sure Hot tier is selected and add Index tags (this enables search based on tags). 

![](./images/L03-003.png)

Copy object URL and try to open it in browser. You will get access denied message since this this container is Private (= require authentication).

![](./images/L03-004.png)

When accessing objects we can use Azure Active Directory authentication (beyond scope of this lab) or simple key/token based authentication. Let's generate SAS token to access this particular object for next 24 hours on read-only manner. Then copy URL with token and open it in browser. Note you can also have tokes with write capabilities etc. so Blob storage can be used by applications to server as well as receive user data without going throw application server.

![](./images/L03-005.png)
![](./images/L03-006.png)

In scripts you can us azcopy. First generate SAS token for whole container with write permissions.

![](./images/L03-007.png)

Install azcopy on you Windows VM and modify following command with your SAS URL to copy files to Blob storage.

```powershell
choco install azcopy10

azcopy copy 'C:\Program Files (x86)\Windows Mail' `
    'https://storetomaskubica5.blob.core.windows.net/cont1?sp=racwdli&st=2022-03-10T12:04:43Z&se=2022-03-11T12:04:43Z&spr=https&sv=2020-08-04&sr=c&sig=khWBMXmRng3ViQSEc8avAU1TNHKCR8iiLAe6wqhJ5eE%3D' `
    --recursive `
    --preserve-smb-permissions=false `
    --preserve-smb-info=true
```

![](./images/L03-008.png)

Note you can filter based on index tags - enter department=finance.

![](./images/L03-009.png)


## Tiering
Azure Blob supports multiple tiers:
- Premium (requires separate storage account) designed for high IOPS even with very small files
- Hot tier for frequently accessed blobs with very low access fees (almost zero) - eg. 20 EUR per TB in North Europe
- Cool tier for less frequently accessed yet online blobs - 9 EUR per TB in North Europe, but payment fee for data acess 
- Archive tier which is offline (rehydration in hours) - just 0,89 EUR per TB in North Europe, but relively high access fees

Use right click on objects to change their tier to Cool and Archive.

![](./images/L03-010.png)

Objects in archive tier cannot be accessed directly via URL, but you can request rehydration by changing tier to Hot or Cool.

You can automate lifecycle of objects to move between tiers (or get deleted) based on last accessed time and filtered per container or index tags.

![](./images/L03-011.png)
![](./images/L03-012.png)
![](./images/L03-013.png)


## Data protection
In your storage account enable point-in-time restore (continuous tracink of all changes) which will also enable blob versioning.

![](./images/L03-014.png)

Create file mydata.txt with content "v1" and upload to container. Then change content to "v2" and upload to container again (rewrite). Now look at your object and note previous versions are stored. You can download previous version, revert change etc.

![](./images/L03-015.png)
![](./images/L03-016.png)

Soft delete is also enabled so first delete this file and then let see list of blobs including deleted ones.

![](./images/L03-017.png)

Sometimes regulation requires for blobs to be immutable - cannot be modified or deleted eg. for certain period of time. This WORM-style (write-once-read-many) solution is also available (look at configuration options, but we will not configure this in our lab).

![](./images/L03-018.png)


## Advanced search
You might use Blob storage for documents, images and other content and build applications that provide users with full text search capabilities, semantic search, autocomplete based on data from multiple sources (Blobs, databases, etc.). You might want to enhance search capabilities with cognitive services such as image recognition and description, entity recognition, translations, OCR and much more. Azure Blob Storage can be easily integrated with Azure Cognitive Search.

Get few PDF files (download something from Internet for example) and upload those to your cont1 container in your Blob storage.

Create new Cognitive Search.

![](./images/L03-019.png)
![](./images/L03-020.png)
![](./images/L03-021.png)

Go back to storage and open configuration wizard.

![](./images/L03-022.png)
![](./images/L03-023.png)

Let indexer run every hour to pick up new blobs.

![](./images/L03-024.png)

Open Cognitive Search and make sure indexer has run successfully. 

![](./images/L03-025.png)
![](./images/L03-026.png)

Try search API.

![](./images/L03-027.png)
![](./images/L03-028.png)
