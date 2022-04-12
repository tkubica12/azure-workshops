## 02 - Basic virtual network
In this lab we will create virtual network with subnets, deploy virtual machines and test connectivity.

First we will create resource group, virtual network with three subnets.

```bash
# Configure prefix (in bash)
export prefix=tomaskubica4

# Configure prefix (in PowerShell)
$prefix="tomaskubica4"

# Create resource group
az group create -n $prefix-project1 -l northeurope

# Create VNET
az network vnet create -n $prefix-project1 -g $prefix-project1 --address-prefix 10.1.0.0/16

# Create three subnets
az network vnet subnet create -n jump     -g $prefix-project1 --vnet-name $prefix-project1 --address-prefixes 10.1.0.0/24
az network vnet subnet create -n frontend -g $prefix-project1 --vnet-name $prefix-project1 --address-prefixes 10.1.1.0/24
az network vnet subnet create -n backend  -g $prefix-project1 --vnet-name $prefix-project1 --address-prefixes 10.1.2.0/24
```

We will now deploy few servers with serial access enabled to test things out. We will have one jump server, two frontend server (each in separate availability zone - different physical datacenters) and one backend.

```bash
# In bash
az storage account create -n seriak$prefix -g $prefix-project1

az vm create -n $prefix-jump \
    -g $prefix-project1 \
    --image UbuntuLTS \
    --vnet-name $prefix-project1 \
    --subnet jump \
    --size Standard_B1s \
    --admin-username labuser \
    --admin-password Azure12345678 \
    --authentication-type password \
    --zone 1 \
    --private-ip-address 10.1.0.10 \
    --public-ip-address "" \
    --nsg "" \
    --boot-diagnostics-storage seriak$prefix \
    --no-wait
az vm create -n $prefix-front1 \
    -g $prefix-project1 \
    --image UbuntuLTS \
    --vnet-name $prefix-project1 \
    --subnet frontend \
    --size Standard_B1s \
    --admin-username labuser \
    --admin-password Azure12345678 \
    --authentication-type password \
    --zone 1 \
    --private-ip-address 10.1.1.11 \
    --public-ip-address "" \
    --nsg "" \
    --boot-diagnostics-storage seriak$prefix \
    --no-wait
az vm create -n $prefix-front2 \
    -g $prefix-project1 \
    --image UbuntuLTS \
    --vnet-name $prefix-project1 \
    --subnet frontend \
    --size Standard_B1s \
    --admin-username labuser \
    --admin-password Azure12345678 \
    --authentication-type password \
    --zone 2 \
    --private-ip-address 10.1.1.12 \
    --public-ip-address "" \
    --nsg "" \
    --boot-diagnostics-storage seriak$prefix \
    --no-wait
az vm create -n $prefix-back \
    -g $prefix-project1 \
    --image UbuntuLTS \
    --vnet-name $prefix-project1 \
    --subnet backend \
    --size Standard_B1s \
    --admin-username labuser \
    --admin-password Azure12345678 \
    --authentication-type password \
    --zone 1 \
    --private-ip-address 10.1.2.10 \
    --public-ip-address "" \
    --nsg "" \
    --boot-diagnostics-storage seriak$prefix \
    --no-wait
```

```powershell
# In PowerShell
az storage account create -n seriak$prefix -g $prefix-project1

az vm create -n $prefix-jump `
    -g $prefix-project1 `
    --image UbuntuLTS `
    --vnet-name $prefix-project1 `
    --subnet jump `
    --size Standard_B1s `
    --admin-username labuser `
    --admin-password Azure12345678 `
    --authentication-type password `
    --zone 1 `
    --private-ip-address 10.1.0.10 `
    --public-ip-address '""' `
    --nsg '""' `
    --boot-diagnostics-storage seriak$prefix `
    --no-wait
az vm create -n $prefix-front1 `
    -g $prefix-project1 `
    --image UbuntuLTS `
    --vnet-name $prefix-project1 `
    --subnet frontend `
    --size Standard_B1s `
    --admin-username labuser `
    --admin-password Azure12345678 `
    --authentication-type password `
    --zone 1 `
    --private-ip-address 10.1.1.11 `
    --public-ip-address '""' `
    --nsg '""' `
    --boot-diagnostics-storage seriak$prefix `
    --no-wait
az vm create -n $prefix-front2 `
    -g $prefix-project1 `
    --image UbuntuLTS `
    --vnet-name $prefix-project1 `
    --subnet frontend `
    --size Standard_B1s `
    --admin-username labuser `
    --admin-password Azure12345678 `
    --authentication-type password `
    --zone 2 `
    --private-ip-address 10.1.1.12 `
    --public-ip-address '""' `
    --nsg '""' `
    --boot-diagnostics-storage seriak$prefix `
    --no-wait
az vm create -n $prefix-back `
    -g $prefix-project1 `
    --image UbuntuLTS `
    --vnet-name $prefix-project1 `
    --subnet backend `
    --size Standard_B1s `
    --admin-username labuser `
    --admin-password Azure12345678 `
    --authentication-type password `
    --zone 1 `
    --private-ip-address 10.1.2.10 `
    --public-ip-address '""' `
    --nsg '""' `
    --boot-diagnostics-storage seriak$prefix `
    --no-wait
```

There are no restrictions currently in our setup, every VM can reach every other. Also there is implicit SNAT to Internet. To exit serial console you type CTRL+] and press q.

```bash
az serial-console connect -n $prefix-jump -g $prefix-project1

# Test connectivity
export prefix=tomaskubica4
ping -c 2 $prefix-front1
ping -c 2 $prefix-front2
ping -c 2 $prefix-back
curl http://ifconfig.io/all

# No broadcast, ARP manupulation etc. - cloud is pure L3 (ARP response generated by hypervisor host router of your VNET)
sudo ip a change 10.1.0.123/24 dev eth0
sudo ip a del 10.1.0.10/24 dev eth0
ping -c 2 $prefix-front1    # FAILS! No broadcast, gARP etc.
sudo ip a del 10.1.0.123/24 dev eth0
sudo dhclient
ping -c 2 $prefix-front1    # OK
```