# 05 - Central connectivity and controls with Azure vWAN and Azure Firewall
Now we will connect this project to overall enterprise network topology with centralized network controls on Azure Firewall vis Azure Virtual WAN.

In this chapter it is often easier to use Azure Portal especially when reviewing firewall rules. This guide is using CLI, but keep looking into Azure Portal to see results.

First we will create another project to play with.

```bash
# Configure prefix (in bash)
export prefix=tomaskubica4

# Configure prefix (in PowerShell)
$prefix="tomaskubica4"

# Create resource group
az group create -n $prefix-project2 -l northeurope

# Create VNET
az network vnet create -n $prefix-project2 -g $prefix-project2 --address-prefix 10.2.0.0/16

# Create subnet
az network vnet subnet create -n machines -g $prefix-project2 --vnet-name $prefix-project2 --address-prefixes 10.2.0.0/24
```

```bash
# Deploy virtual machine (in bash)
az storage account create -n seriak2$prefix -g $prefix-project2

az vm create -n $prefix-vm \
    -g $prefix-project2 \
    --image UbuntuLTS \
    --vnet-name $prefix-project2 \
    --subnet machines \
    --size Standard_B1s \
    --admin-username labuser \
    --admin-password Azure12345678 \
    --authentication-type password \
    --zone 1 \
    --private-ip-address 10.2.0.10 \
    --public-ip-address "" \
    --nsg "" \
    --boot-diagnostics-storage seriak2$prefix \
    --no-wait
```

```powershell
# Deploy virtual machine (in PowerShell)
az storage account create -n seriak2$prefix -g $prefix-project2

az vm create -n $prefix-vm `
    -g $prefix-project2 `
    --image UbuntuLTS `
    --vnet-name $prefix-project2 `
    --subnet machines `
    --size Standard_B1s `
    --admin-username labuser `
    --admin-password Azure12345678 `
    --authentication-type password `
    --zone 1 `
    --private-ip-address 10.2.0.10 `
    --public-ip-address '""' `
    --nsg '""' `
    --boot-diagnostics-storage seriak2$prefix `
    --no-wait
```

Check routing table of project2 NIC. Note there is no connection to our other private networks.

```bash
az network nic show-effective-route-table -g $prefix-project2 -n $prefix-vmVMNic -o table
```

Add project1 and project2 to our vWAN hub.

```bash
# Add project1 to hub (in bash)
az network vhub connection create -n project1conn \
    -g $prefix-central \
    --vhub-name $prefix-ne-hub \
    --remote-vnet $(az network vnet show -n $prefix-project1 -g $prefix-project1 --query id -o tsv)

# Add project2 to hub
az network vhub connection create -n project2conn \
    -g $prefix-central \
    --vhub-name $prefix-ne-hub \
    --remote-vnet $(az network vnet show -n $prefix-project2 -g $prefix-project2 --query id -o tsv)
```

```powershell
# Add project1 to hub (in PowerShell)
az network vhub connection create -n project1conn `
    -g $prefix-central `
    --vhub-name $prefix-ne-hub `
    --remote-vnet $(az network vnet show -n $prefix-project1 -g $prefix-project1 --query id -o tsv)

# Add project2 to hub
az network vhub connection create -n project2conn `
    -g $prefix-central `
    --vhub-name $prefix-ne-hub `
    --remote-vnet $(az network vnet show -n $prefix-project2 -g $prefix-project2 --query id -o tsv)
```

Check project2 NIC routing table again. You will now see hub network being directly peered (VnetPeering) while project1 network is routed via hub router (VirtualNetworkGateway).

```bash
az network nic show-effective-route-table -g $prefix-project2 -n $prefix-vmVMNic -o table
```

Check vWAN hub router default table that we are using with both connections.

```bash
# Check routing in hub (in bash)
az network vhub get-effective-routes -g $prefix-central -n $prefix-ne-hub --resource-type RouteTable -o table \
    --resource-id $(az network vhub route-table show -n defaultRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)
```

```powershell
# Check routing in hub (in PowerShell)
az network vhub get-effective-routes -g $prefix-central -n $prefix-ne-hub --resource-type RouteTable -o table `
    --resource-id $(az network vhub route-table show -n defaultRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)
```

So we now have connectivity via router (traffic is not routed via firewall yet). Let's try this.

```bash
az serial-console connect -n $prefix-vm -g $prefix-project2
ping -c 2 10.1.0.10   # jump in project1
```

Before we implement firewalling let's create private DNS zone that would span all our projects. In enterprise networks you might also want to bring your own DNS server for additional features.

```bash
# Add DNS zone, link it to VNETs and print records (in bash)
az network private-dns zone create -n $prefix.cz -g $prefix-central
az network private-dns link vnet create -n $prefix-project1 \
    -g $prefix-central \
    --virtual-network $(az network vnet show -n $prefix-project1 -g $prefix-project1 --query id -o tsv) \
    --registration-enabled \
    --zone-name $prefix.cz
az network private-dns link vnet create -n $prefix-project2 \
    -g $prefix-central \
    --virtual-network $(az network vnet show -n $prefix-project2 -g $prefix-project2 --query id -o tsv) \
    --registration-enabled \
    --zone-name $prefix.cz

az network private-dns record-set a list -g $prefix-central -z $prefix.cz
```

```powershell
# Add DNS zone, link it to VNETs and print records (in PowerShell)
az network private-dns zone create -n $prefix.cz -g $prefix-central
az network private-dns link vnet create -n $prefix-project1 `
    -g $prefix-central `
    --virtual-network $(az network vnet show -n $prefix-project1 -g $prefix-project1 --query id -o tsv) `
    --registration-enabled `
    --zone-name $prefix.cz
az network private-dns link vnet create -n $prefix-project2 `
    -g $prefix-central `
    --virtual-network $(az network vnet show -n $prefix-project2 -g $prefix-project2 --query id -o tsv) `
    --registration-enabled `
    --zone-name $prefix.cz

az network private-dns record-set a list -g $prefix-central -z $prefix.cz
```

Test DNS.

```bash
az serial-console connect -n $prefix-vm -g $prefix-project2
export prefix=tomaskubica4
ping -c 2 $prefix-jump.$prefix.cz
```

We will now modify routing so all communications from projects to Internet or between projects are going via firewall (note that you can also do the same for traffic to on-prem via VPN or Express Route in your hub).

```bash
# Route rfc1918 and default via firewall (in bash)
az network vhub route-table route add -n defaultRouteTable \
    --route-name all_traffic \
    -g $prefix-central \
    --vhub-name $prefix-ne-hub \
    --destination-type CIDR --destinations "0.0.0.0/0" "10.0.0.0/8" "172.16.0.0/12" "192.168.0.0/16" \
    --next-hop-type ResourceId \
    --next-hop $(az network firewall show -n $prefix-fw -g $prefix-central --query id -o tsv)
```

```powershell
# Route rfc1918 and default via firewall (in PowerShell)
az network vhub route-table route add -n defaultRouteTable `
    --route-name all_traffic `
    -g $prefix-central `
    --vhub-name $prefix-ne-hub `
    --destination-type CIDR --destinations "0.0.0.0/0" "10.0.0.0/8" "172.16.0.0/12" "192.168.0.0/16" `
    --next-hop-type ResourceId `
    --next-hop $(az network firewall show -n $prefix-fw -g $prefix-central --query id -o tsv)
```

Check routing in hub - our route is configured, but there are still more specific routes to projects which will take precedence (longest prefix match).

```bash
# Check routing in hub (in bash)
az network vhub get-effective-routes -g $prefix-central -n $prefix-ne-hub --resource-type RouteTable -o table \
    --resource-id $(az network vhub route-table show -n defaultRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)
```

```powershell
# Check routing in hub (in PowerShell)
az network vhub get-effective-routes -g $prefix-central -n $prefix-ne-hub --resource-type RouteTable -o table `
    --resource-id $(az network vhub route-table show -n defaultRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)
```

To remove specific routes to projects we will now disable route propagation on network connection.

```bash
# Do not propage to default route table (in bash)
az network vhub connection update -n project1conn -g $prefix-central --vhub-name $prefix-ne-hub --labels "" \
    --propagated $(az network vhub route-table show -n noneRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)
az network vhub connection update -n project2conn -g $prefix-central --vhub-name $prefix-ne-hub --labels "" \
    --propagated $(az network vhub route-table show -n noneRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)
```

```powershell
# Do not propage to default route table (in PowerShell)
az network vhub connection update -n project1conn -g $prefix-central --vhub-name $prefix-ne-hub --labels '""' `
    --propagated $(az network vhub route-table show -n noneRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)
az network vhub connection update -n project2conn -g $prefix-central --vhub-name $prefix-ne-hub --labels '""' `
    --propagated $(az network vhub route-table show -n noneRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)
```

Check routing tables now.

```bash
# Check routing in hub (in bash)
az network vhub get-effective-routes -g $prefix-central -n $prefix-ne-hub --resource-type RouteTable -o table \
    --resource-id $(az network vhub route-table show -n defaultRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)
```

```powershell
# Check routing in hub (in PowerShell)
az network vhub get-effective-routes -g $prefix-central -n $prefix-ne-hub --resource-type RouteTable -o table `
    --resource-id $(az network vhub route-table show -n defaultRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)
```

We can now check Firewall is blocking our communications to other projects and to Internet.

```bash
az serial-console connect -n $prefix-vm -g $prefix-project2
export prefix=tomaskubica4
ping -c 2 $prefix-jump.$prefix.cz   # Firewall blocks communication to other projects
curl http://ifconfig.io/all         # Firewall transparent proxy blocks this and injects error message
```

In next chapter we will configure firewall to allow connections we need.