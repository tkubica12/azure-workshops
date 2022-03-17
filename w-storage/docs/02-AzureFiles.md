# Lab 2 - Network Attached Storage options with Azure Files
In this lab we will focuse on remote file systems as a service, namely Azure Files (not that for very low-latency high-performance scenarios you can also leverage Azure NetApp Files).

## Using shares as a service

Create storage account and keep everything on defaults.

![](./images/L02-001.png)
![](./images/L02-002.png)
![](./images/L02-003.png)

Open storage account and create new share.

![](./images/L02-004.png)

Get script to mount your share in your Windows VM in Azure. Note we will use account keys in this lab, but in enterpise environment you can use Active Directory logins and ACLs.

![](./images/L02-005.png)

Paste this script into PowerShell sesion on your Azure VM, see you can get access to share, create file data.txt and write "v1" to it.

![](./images/L02-006.png)

Now let's create snapshot via Azure portal.

![](./images/L02-007.png)
![](./images/L02-008.png)

Modify data.txt.

![](./images/L02-009.png)

Go to Azure portal and see your snapshot. Note you can download individual file to your PC or restore individual file on share.

![](./images/L02-010.png)

You can also get script to map snapshot as share to your Windows VM.

![](./images/L02-011.png)
![](./images/L02-012.png)

Note using Azure Backup to orchestrate this capability is strongly advised.

## Hybrid scenarios with replication from on-premises

Now we will Azure Files Sync feature to synchronize on-premises file share with Azure Files:
- Bringing files to central location in cloud enables backup adn DR capability and ability to access files also in cloud due to two-way synchronization (great for hybrid scenarios)
- On-prem systems can also do tiering extending beyond its physical capacity without need to install more local space (share works then like a cache for cloud data without need to do any changes in application that still can get all cached and cloud data via local Windows endpoint)
- Multi-to-one scenario is supported (eg. centralization of data from branches or stores)

We will use are Windows VM to simulate on-premises system. Create folder onprem (optionaly you can configure traditional share on this folder - not required for our lab today).

![](./images/L02-013.png)

Prepare our "on-premises" server by installing browser and PowerShell modules in your Azure VM.

```powershell
choco install firefox
choco install az.powershell

$AdminKey = "HKLM:\SOFTWARE\Microsoft\Active Setup\Installed Components\{A509B1A7-37EF-4b3f-8CFC-4F3A74704073}"
$UserKey = "HKLM:\SOFTWARE\Microsoft\Active Setup\Installed Components\{A509B1A8-37EF-4b3f-8CFC-4F3A74704073}"
Set-ItemProperty -Path $AdminKey -Name "IsInstalled" -Value 0
Set-ItemProperty -Path $UserKey -Name "IsInstalled" -Value 0
Stop-Process -Name Explorer
```

Then download Azure Files Sync installation file for WS2019, run and and keep everything on defaults. After you click Finish, configuration wizard will come up - stop there for now as we need to prepare Azure side.

```
https://go.microsoft.com/fwlink/?linkid=858257
```

Deploy Azure Files Sync resource in Azure.

![](./images/L02-014.png)
![](./images/L02-015.png)
![](./images/L02-016.png)

Create Sync Group with our existing Azure Files share.

![](./images/L02-017.png)
![](./images/L02-018.png)

Now finish server configuration. Sign in to Azure and register server with Azure Files Sync.

![](./images/L02-019.png)
![](./images/L02-020.png)

Server should now show up in Azure portal. Add it to your sync group. Because we use folder on C: we cannot enable cloud tiering (only 1:1 sync), but that is fine for this lab.

![](./images/L02-021.png)
![](./images/L02-022.png)
![](./images/L02-023.png)

We can now see data from Azure Files synced to our local folder (data.txt). Create local file and make sure it gets replicated to Azure Files.

![](./images/L02-024.png)
![](./images/L02-025.png)

