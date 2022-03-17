# Lab 1 - Azure Disks for your Virtual Machines and containers
In this lab we will focus on remote raw block storage devices for your compute resources - Azure Disks.

## Prepare lab environment

Whole group will share one virtual network and Bastion service that enables us to securely access RDP of our machines vai Azure Portal without exposing VMs directly to Internet. Following commands are here for reference and instructor already prepared this for you.

```powershell
# Shared Virtual Network and Bastion
az group create -n w-storage-shared-rg -l northeurope
az network vnet create -g w-storage-shared-rg -n w-storage-shared-vnet --address-prefixes 10.0.0.0/16
az network vnet subnet create -g w-storage-shared-rg --vnet-name w-storage-shared-vnet -n virtualmachines --address-prefixes 10.0.0.0/22
az network vnet subnet create -g w-storage-shared-rg --vnet-name w-storage-shared-vnet -n AzureBastionSubnet  --address-prefixes 10.0.4.0/24
az network public-ip create -g w-storage-shared-rg  -n bastion-ip --sku Standard --location northeurope
az network bastion create -n bastion --public-ip-address bastion-ip -g w-storage-shared-rg --vnet-name w-storage-shared-vnet --location northeurope
```

Use CLI to create Windows virtual machine with username workshop and password Azure12345678.

```powershell
# Configure prefix as yourname+number
$prefix="tomaskubica5"

# Create Resource Group
az group create -n $prefix-rg -l northeurope

# Create Virtual Machine
az vm create -n $prefix-vm `
    -g $prefix-rg `
    --computer-name $prefix `
    --image Win2019Datacenter `
    --admin-username workshop `
    --admin-password Azure12345678 `
    --size Standard_D2as_v4 `
    --nic-delete-option Delete `
    --public-ip-address '""' `
    --subnet $(az network vnet subnet show -g w-storage-shared-rg --vnet-name w-storage-shared-vnet -n virtualmachines --query id -o tsv) `
    --zone 3
```

Use Azure Portal to access this VM.

![](./images/L01-001.png)
![](./images/L01-002.png)
![](./images/L01-003.png)

Some VM types come with local temporary storage as in our case.

## Basic usage of Azure Disk

Use Azure Portal to create new Azure Disk which is remote storage option (LRS disks are stored in three synchronous copies spread across different storage nodes while ZRS disks are stored in three synchronous copies spread over three separate availability zones - DCs).

![](./images/L01-004.png)
![](./images/L01-005.png)
![](./images/L01-006.png)
![](./images/L01-007.png)

Click on Change size and investigate different options and performance characteristics.

![](./images/L01-008.png)

Create two disks:
- LRS Standard SSD disk with size 1 TB
- LRS Premium SSD disk with size 1 TB

Attach your new disks to your virtual machine.

![](./images/L01-009.png)
![](./images/L01-010.png)
![](./images/L01-011.png)

You should see new devices now in your server.

![](./images/L01-012.png)

Right click on disks and initialize and format both disks.

![](./images/L01-013.png)
![](./images/L01-014.png)

## Performance characteristics of Azure Disk

Let's compare performance of both disks. For simplicity we will focus our test on IOPS - note that you need to configure test differently to measure latency (0 outstanding IOs) or throughput (more workers or even larger block size).

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

choco install iometer
```

![](./images/L01-015.png)
![](./images/L01-016.png)
![](./images/L01-017.png)
![](./images/L01-018.png)
![](./images/L01-019.png)

Repeat for second disk.

![](./images/L01-020.png)

## Disk snapshots

Write some file to one of your disks.

![](./images/L01-021.png)

We will now create snapshot - we should disconnect disk first to make sure file-system consistency level, but for our lab we are fine with crash-consistent snapshot. Go to Azure portal and create snapshot of your disk. Note we can use incrementals snapshot or full one and also place it on zone-redundant storage so we can recover to any zone.

![](./images/L01-022.png)

Open your snapshot and use it to create new disk.

![](./images/L01-023.png)

Attach this disk to your VM, bring it online and make sure you can see your data.

![](./images/L01-024.png)
![](./images/L01-025.png)
![](./images/L01-026.png)
![](./images/L01-027.png)

Note most often customers use Azure Backup service to orchestrate things like backup operations, one-click recovery, long-term backup storage and application-consistent backups (using volume shadow copy feature in Windows). Azure Backup is levaraging multiple technologies including disk snapshots under covers.


