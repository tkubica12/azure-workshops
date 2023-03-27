# Azure Files demo with AD integration

1. Deploy demo infrastructure with ```terraform apply -var existing_admin_password=mypassword```
2. Use Bastion to connect to admin VM using fadmin@tkubica.biz account and password stored in Key Vault
3. From admin VM join storage account to domain using PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
Install-Module -Name Az -Scope CurrentUser -Repository PSGallery -Force
Invoke-WebRequest https://github.com/Azure-Samples/azure-files-samples/releases/download/v0.2.5/AzFilesHybrid.zip -OutFile AzFilesHybrid.zip
Expand-Archive AzFilesHybrid.zip -DestinationPath .
.\CopyToPSPath.ps1
Import-Module -Name AzFilesHybrid
Connect-AzAccount -UseDeviceAuthentication

$SubscriptionId = "d3b7888f-c26e-4961-a976-ff9d5b31dfd3"
$ResourceGroupName = "d-storage-files"
$StorageAccountName = "xorqwwfm"
$SamAccountName = "xorqwwfm"

Select-AzSubscription -SubscriptionId $SubscriptionId 
Join-AzStorageAccount -ResourceGroupName $ResourceGroupName -StorageAccountName $StorageAccountName -SamAccountName $SamAccountName

Debug-AzStorageAccountAuth -StorageAccountName $StorageAccountName -ResourceGroupName $ResourceGroupName -Verbose
```
4. Connect to vm1 as fuser1@tkubica.biz with password from Key Vault
5. Map drive shared key (admin access) to setup ACLs
```powershell
cmd.exe /C "cmdkey /add:`"xorqwwfm.file.core.windows.net`" /user:`"localhost\xorqwwfm`" /pass:`"t6vwmDDZIufMN7GLP9OUReVK7atDFO5NnnD+aEu9nIVDpn/6SDAak1hIsUrUZA6h46vf2jZBninb+AStxmzC5w==`""

New-PSDrive -Name G -PSProvider FileSystem -Root "\\xorqwwfm.file.core.windows.net\share1" -Persist
```

6. Create directories and ACLs, check results in UI

```powershell
cmd
mkdir G:\diruser1
icacls G:\diruser1 /grant fuser1@tkubica.biz:(d,wdac)
mkdir G:\diruser2
icacls G:\diruser2 /grant fuser2@tkubica.biz:(d,wdac)
```

7. Connect to vm2 as fuser2@tkubica.biz with password from Key Vault
8. Map drive -> you should see only diruser2 directory

```powershell
New-PSDrive -Name Y -PSProvider FileSystem -Root "\\xorqwwfm.file.core.windows.net\share1" -Persist
```