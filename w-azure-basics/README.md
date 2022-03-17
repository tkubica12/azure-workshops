# Basic Azure workshop

- [Basic Azure workshop](#basic-azure-workshop)
- [1. Connect to Azure portal a observe types of services available](#1-connect-to-azure-portal-a-observe-types-of-services-available)
- [2. Use cloud shell and CLI to quickly create VM and connect, observe created resources](#2-use-cloud-shell-and-cli-to-quickly-create-vm-and-connect-observe-created-resources)
- [3. Prepare new network with load balancer](#3-prepare-new-network-with-load-balancer)
- [4. Create new VM using wizard and discuss various options and settings](#4-create-new-vm-using-wizard-and-discuss-various-options-and-settings)
- [5. Connect VNETs to enteprise network architecture](#5-connect-vnets-to-enteprise-network-architecture)
- [6. Storage](#6-storage)
- [7. Database as a service](#7-database-as-a-service)
- [8. Monitoring](#8-monitoring)
- [9. Automation with Terraform](#9-automation-with-terraform)


# 1. Connect to Azure portal a observe types of services available
1. Connect to Azure
2. Suggest to switch to English, select your color theme etc - use configuration icon in top right corner
3. In top left corner click on menu button and select All services - discuss what services are available
4. Create new Resource Group - eg. by using + Create a resource in left menu or search in global search on top in middle for resource group and click Create
5. Create resource group called "yourname" (eg. tomaskubica) in region West Europe
6. Open Resource Group and got to Access Control (IAM)
7. Discuss scope (tenant, management group, subscription, resource group, resource), role (and its permissions) and identity
8. On scope of your resource group add in role "Reader" to Managed Identity -> User-assigned managed identity -> "workshop-identity"
9. On your resource group go to Budget and Add one - monthly ammount, then set alert type Actual for 90% (triggers when you spend 90%) and of type Forecasted to 120% (triggers when you spend too fast and monthly forecast is over 120%); note appart from email you can use Action Group for complex actions including custom code

# 2. Use cloud shell and CLI to quickly create VM and connect, observe created resources
1. Go to portal and click on shell icon or open new page at [shell.azure.com](https://shell.azure.com) for Bash or [shell.azure.com/powershell](https://shell.azure.com/powershell) for PowerShell
2. (bash option) Change name to match your resource group in first command and run this

```bash
export name=tomaskubica

az vm create --name $name-vm1 \
    --resource-group $name \
    --image UbuntuLTS \
    --admin-username azureuser \
    --admin-password Azure12345678 \
    --authentication-type password \
    --size Standard_B2s

export ip=$(az vm list-ip-addresses -g $name -n $name-vm1 --query [0].virtualMachine.network.publicIpAddresses[0].ipAddress -o tsv)
ssh azureuser@$ip
```

2. (PowerShell option) Change name to match your resource group in first command and run this

```powershell
$name="tomaskubica2"

New-AzVm `
    -ResourceGroupName $name `
    -Name "$name-vm1" `
    -Credential (Get-Credential) `
    -Size "Standard_B2s" 
```

Go to portal, focus on search bar (or press g/) and type your name to search for VM. Click on it, then click on "Connect" button and download RDP file.

3. Open portal, find your resource group eg. via global search on top (also via g/ shortcut), All resources (via left top menu or ga shortcut), via Resource Groups (or gr shortcut) etc.
4. Investigate objects there - virtual network, network security group, NIC, disk, VM

This demonstrates how to quickly setup compute, storage and networking. In next sections we will go deeper customize thos to fit our enterprise needs.

# 3. Prepare new network with load balancer
1. Create new virtual network with IP range 10.x.0.0/16 where is x is assigned to you by instructor
2. Create subnet in this virtual network with name "default" and IP range 10.x.0.0/24
3. Create new load balancer:
   - Page1:
    - Name: yourname-lb
    - SKU: Standard
    - Type: Public
    - Tier: Regional
  - Page2:
      - Add frontend configuration with name "frontend"
      - Create new public IP named "yourname-ip" and make it Zone-redundant (zone is isolated environment, such as DC building, make IP work across those - metro solution)
  - Page3:
      - Add backend pool called "backend", point it to your VNET (no VMs will be added at this point) 
  - Page4:
      - Add load balancing rule called "webrule", select frontend ip, backend pool, both ports 80 and create new health probe with http protocol
      - **Important:** set "Outbound source network address translation (SNAT)" to "Use implicit outbound rule. This is not recommended because it can cause SNAT port exhaustion" so this LB can provide Internet access to your VM and we do not need to configure outbound rules explicitely
  - Skip all other pages and click Review and Create

# 4. Create new VM using wizard and discuss various options and settings
1. Open Create New VM wizard (eg. open Virtual Machines via global search and click on Create)
2. Name of VM will be "yourname-web1"
3. Select West Europe region and discuss what regions are available
4. Select Availability Zone in Availability Options, select zone 1 and discuss what zones are and why it is important
5. Keep image on Ubuntu 18.04 and Security on Standard (discuss with instructor what other options mean)
6. Click on See all sizes and select Standard_B1s and discuss what types of machines are available and where to find more details
7. Configure password authentication
8. Enable port 80 inbound, but not SSH
9. On next page do not change disks - we will discus storage later
10. In networking make sure you are connected to right VNET
11. Select None on public IP
12. In load balancing let this VM to be added to your LB
13. On management page change Boot diagnostics to "Enable with custom storage account" and let new account be created (we need this for serial console access)
14. Discuss other options here (authentication, backups, patching)
15. In advanced section let's add Custom data (cloud-init) so web server is isntalled automatically:
    
```bash
#!/bin/bash
sudo apt update && sudo apt install nginx -y
echo "Hello from WEB 1" | sudo tee /var/www/html/index.html
```

16. Discuss reservations, dedicated hosts and other options
17. Finish wizard and create VM
18. Make sure you can access web from Load Balancer public IP
19. Now repeat process to add second VM - make sure name and string in script (steps 2 and 15) and also in step 4 select different zone (eg. zone 2)
20. Connect to Load Balancer public IP from multiple tabs or use curl - you should see responses coming from different servers

Troubleshooting tips:
- Has web server been sucessfully installed? Connect to VM using Serial Console via portal a check it out (curl 127.0.0.1).
- Are health probes failing? Look at Load Balancer in portal in Insights section.
- Make sure your VM and LB is in the same VNET.

# 5. Connect VNETs to enteprise network architecture
1. In portal find workshop-vwan in shared-workshop-resources resource group
2. Go to Virtual network connections and add your VNET to workshop-hub
3. Access your VM via Serial Port - either go to portal, VM and Serial Console or via cloud shell issue command "az serial-console connect -n yourvm -g yourrg"
4. Check you can access shared web at 10.254.0.100 (curl 10.254.0.100) - note it can take few minutes for routes to come up after adding your VNET to hub
5. Find NIC of your VM and select Effective Routes to see routing table

# 6. Storage
1. Create new Azure Disk (eg. find Azure Disk in search and click Create or click on Create new resource in top left menu)
2. Use region West Europe
3. Click on Change size and discuss various options here (LRS vs. ZRS, Standard HDD vs. Standard SSD vs. Premium SSD vs. Ultra SSD) - then select small Standard SSD disk
4. Discuss encryption
5. Discuss shared disks
6. Attach new data disk to your VM -> go to your VM, Disks and click on Attach existing disks
7. Connect to VM and observe new raw device, also discuss temp disk with some VM types or NVMe
8. Create new Storage Account
9. Discuss Standard vs. Premium -> select Standard
10. Discuss redundancy options - LRS vs. ZRS vs. GRS vs. GZRS -> select LRS
12. On Networking page keep access public for now
13. Discuss other options (version, lifecycle, tiers) and create storage
14. Go to Containers, create private container and upload JPEG file
15. Click on file, go to Generate SAS and copy resultion URL with token to browser - your image should be displayed
16. Select file and change its tier to Archive (offline store) to save costs
17. Go to File shares, create new one, go in and click Connect to generate mounting script for your VM (using SMB/CIFS)
18. Note Premium Files storage account support also NFS 4.1 mounting
19. Note storage with hierarchical namespace enabled supports access to Blobs (object store) using NFS 3.0, SFTP or driver for HDFS
20. Note for specialized NAS performance needs (eg. ultra low latency or high IOPS to capacity ration) you can use Azure NetApp Files (specialized HW-based solution)

# 7. Database as a service
1. Go to + Create a resource and go to Database section; observe available 1st party options there and discuss with instructor
2. Create SQL Database
3. In server section click on Create New
4. Choose globally unique name 
5. Choose Use only Azure Active Directory (Azure AD) authentication (which includes SSO, MFA and privileged access management) and select yourself as admin
6. In Compute + storage click on Configure Database and discuss available deployment models - then let's continue with serverless option
7. In Networking section enable public access and Add current client IP address to whitelist yourself
8. In security discuss various options and look at Transparent Data Encryption (by default encrypted by Microsoft managed key, but you can use your own)
9. In Data source use Sample and Create database
10. After deployment click on Database and Query Editor, login as Azure Active Directory user and see tables (whitelist IP if needed)
11. Go to Compute + Storage and note you can migrate between sizes and models online
12. Database can run in 3 different building in your region (availability zones) and with Business Critical tier you can use read replicas for read operations. If you need to you can add async replica to different region - Replicas.
13. In Overview section click on Restore button and se how you can do point-in-time restore to different DB

# 8. Monitoring
1. Your subscription has been configured with Policy to autoenroll to Azure Monitor and Security Center
2. Go to Inventory and Change tracking and observe
3. Backup your VM to existing backup vault in shared-workshop-resources resource group
4. Go to Insights and see Health, Performance and Map
5. Go to Logs and search Syslog (Linux) or Event (Windows) table
6. Open Azure Monitor and look at categories including Application, SQL or Network
7. Go to Service Health to understand how incidents and maintenance are communicated
8. Go to Security Center and explore recommendations, vulnerabilities, missing updates etc.
9. Go to Azure Sentinel and see Data sources, Azure Activity in Workbook section. Go to Hunting and check for various queries such as AzureActivity, AWS, ...

# 9. Automation with Terraform
In this lab we will deploy network, load balancer and farm of web servers similar to before, but this time autometed with Infrastructure as Code. Native Azure Bicep, Terraform and Pulumi comes with deep support for Azure, but you can also leverage Crossplane (Kubernetes-style declarative model), Ansible (more imperative style). Usualy Bicep or Terraform is prefered - in our lab we will use Terraform because of its hybrid and multi-cloud capabilities.

1. Open cloud shell and clone this repo

```bash
git clone https://github.com/tkubica12/workshop-feb22.git
```

2. Modify file terraform.tfvars and put your name there (prefix=yourname)
3. Initialize Terraform and run plan to see what will be added

```bash
cd resoucres/automation
terraform init
terraform plan
```

4. Deploy solution

```bash
terraform apply -auto-approve
```

5. Check solution works (you can access LB IP and check servers are balanced)
6. Modify terraform.tfvars and change serverCount to 3
7. Run terraform plan and see output (Terraform will keep existing resources and add new ones), then deploy solution

Notes:
- There is more native way to deploy number of unified servers such as in our scenario as single resource - Virtual Machine Scale Sets. But for our automation purposes we used single machines.
- You definitely should split parts of solution to version controlled reusable modules, create environment specific setting ets. But added complexity is beyond our todays workshop - you might look at my more complex scenario at [https://github.com/tomas-iac](https://github.com/tomas-iac)
