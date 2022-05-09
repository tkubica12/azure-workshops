# 09 - Bring your own hybrid DNS services
In next step we will deploy shared resources such as custom DNS server for conditional forwarding to on-premises and configure hybrid DNS infrastructure.

Similarily to DMZ we will now create separate VNET for shared services (custom DNS service, AD controller, deployment systems etc.) and connect it to our hub.

```bash
# Configure prefix (in bash)
export prefix=tomaskubica4

# Configure prefix (in PowerShell)
$prefix="tomaskubica4"

# Create resource group
az group create -n $prefix-shared -l northeurope

# Create VNET
az network vnet create -n $prefix-shared -g $prefix-shared --address-prefix 10.252.0.0/16

# Create subnet
az network vnet subnet create -n machines -g $prefix-shared --vnet-name $prefix-shared --address-prefixes 10.252.0.0/24
```

We will now deploy virtual machine to be used as DNS server later.

```bash
# Deploy virtual machine (in bash)
az storage account create -n seriak3$prefix -g $prefix-shared

az vm create -n $prefix-dnssrv \
    -g $prefix-shared \
    --image UbuntuLTS \
    --vnet-name $prefix-shared \
    --subnet machines \
    --size Standard_D2a_v4 \
    --admin-username labuser \
    --admin-password Azure12345678 \
    --authentication-type password \
    --zone 1 \
    --private-ip-address 10.252.0.10 \
    --public-ip-address "" \
    --nsg "" \
    --boot-diagnostics-storage seriak3$prefix \
    --no-wait
```

```powershell
# Deploy virtual machine (in PowerShell)
az storage account create -n seriak3$prefix -g $prefix-shared

az vm create -n $prefix-dnssrv `
    -g $prefix-shared `
    --image UbuntuLTS `
    --vnet-name $prefix-shared `
    --subnet machines `
    --size Standard_B1s `
    --admin-username labuser `
    --admin-password Azure12345678 `
    --authentication-type password `
    --zone 1 `
    --private-ip-address 10.252.0.10 `
    --public-ip-address '""' `
    --nsg '""' `
    --boot-diagnostics-storage seriak3$prefix `
    --no-wait
```

Connect shared environment to hub.

```bash
# Add shared to hub (in bash)
az network vhub connection create -n sharedconn \
    -g $prefix-central \
    --vhub-name $prefix-ne-hub \
    --remote-vnet $(az network vnet show -n $prefix-shared -g $prefix-shared --query id -o tsv) \
    --labels "" \
    --propagated $(az network vhub route-table show -n noneRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)
```

```powershell
# Add shared to hub (in PowerShell)
az network vhub connection create -n sharedconn `
    -g $prefix-central `
    --vhub-name $prefix-ne-hub `
    --remote-vnet $(az network vnet show -n $prefix-shared -g $prefix-shared --query id -o tsv) `
    --labels '""' `
    --propagated $(az network vhub route-table show -n noneRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)
```

We will now link our private DNS zones in Azure to this shared VNET and install DNS services in our VM including configuration of forwarding to Azure (and to on-prem, but that is not part of our lab). 

```bash
# In Bash

# Link blob storage privatelink DNS zone
az network private-dns link vnet create \
    -g $prefix-central \
    --zone-name "privatelink.blob.core.windows.net" \
    --name sharedbloblink \
    --virtual-network $(az network vnet show -n $prefix-shared -g $prefix-shared --query id -o tsv) \
    --registration-enabled false

# Link blob storage privatelink DNS zone
az network private-dns link vnet create \
    -g $prefix-central \
    --zone-name $prefix.cz \
    --name $prefix-link \
    --virtual-network $(az network vnet show -n $prefix-shared -g $prefix-shared --query id -o tsv) \
    --registration-enabled false
```

```powershell
# In PowerShell

# Link blob storage privatelink DNS zone
az network private-dns link vnet create `
    -g $prefix-central `
    --zone-name "privatelink.blob.core.windows.net" `
    --name sharedbloblink `
    --virtual-network $(az network vnet show -n $prefix-shared -g $prefix-shared --query id -o tsv) `
    --registration-enabled false

# Link blob storage privatelink DNS zone
az network private-dns link vnet create `
    -g $prefix-central `
    --zone-name "$prefix.cz" `
    --name $prefix-link `
    --virtual-network $(az network vnet show -n $prefix-shared -g $prefix-shared --query id -o tsv) `
    --registration-enabled false
```

Configure DNS server

```bash
az serial-console connect -n $prefix-dnssrv -g $prefix-shared
sudo -i
export prefix=tomaskubica4
apt install -y bind9

cat << EOF > /etc/bind/db.onpremcz
\$TTL 60
@            IN    SOA  localhost. root.localhost.  (
                          2015112501   ; serial
                          1h           ; refresh
                          30m          ; retry
                          1w           ; expiry
                          30m)         ; minimum
                   IN     NS    localhost.
localhost       A   127.0.0.1
test.onprem.cz.   A       172.16.5.5
EOF

cat << EOF > /etc/bind/named.conf.options
options {
        directory "/var/cache/bind";

        // Default forwarder is Azure DNS
        forwarders {
                168.63.129.16;
        };

        listen-on port 53 { any; };
        allow-query { any; };
        recursion yes;

        auth-nxdomain no;    # conform to RFC1035
};
EOF

cat << EOF > /etc/bind/named.conf.local
// onprem zone
zone "onprem.cz" {
  type master;
  file "/etc/bind/db.onpremcz";
};

// forward to Azure node for private link database
zone "privatelink.blob.core.windows.net" {
        type forward;
        forwarders {168.63.129.16;};
};

// forward to Azure node for Azure zone
zone "$prefix.cz" {
        type forward;
        forwarders {168.63.129.16;};
};
EOF

systemctl restart bind9
```

Configure Azure Firewall to be used as DNS proxy for our DNS server. Then reconfigure VNETs to use Azure Firewall as DNS. Note as all DNS requests than go via Azure Firewall -> Your custom DNS server -> forwarding to either Azure or onprem we do not need to map our Azure Private DNS zones to our projects VNET - mapping to VNET with your custom DNS server is sufficient.

```bash
# Enable DNS proxy on Azure Firewall
az network firewall policy update -n $prefix-fw-policy -g $prefix-central --enable-dns-proxy true --dns-servers 10.252.0.10

# Configure VNETs to use Azure Firewall as DNS
az network vnet update -n $prefix-project1 -g $prefix-project1 --dns-servers $(az network firewall show -n $prefix-fw -g $prefix-central --query hubIpAddresses.privateIpAddress -o tsv)
az network vnet update -n $prefix-project2 -g $prefix-project2 --dns-servers $(az network firewall show -n $prefix-fw -g $prefix-central --query hubIpAddresses.privateIpAddress -o tsv)
az network vnet update -n $prefix-dmz -g $prefix-dmz --dns-servers $(az network firewall show -n $prefix-fw -g $prefix-central --query hubIpAddresses.privateIpAddress -o tsv)
az network vnet update -n $prefix-shared -g $prefix-shared --dns-servers $(az network firewall show -n $prefix-fw -g $prefix-central --query hubIpAddresses.privateIpAddress -o tsv)
```

We can now test our DNS configuration - make sure you renew your DHCP lease and check our "onprem" zone is responding.

```bash
az serial-console connect -n $prefix-jump -g $prefix-project1
sudo dhclient -r
sudo dhclient
dig test.onprem.cz
```