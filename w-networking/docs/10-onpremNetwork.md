## 10 - Connect on-premises networks
In last step we will use VPN to setup connection to on-premises networks.

Create VNET and VM that will simulate onprem and onprem router/VPN device.

```bash
# Configure prefix (in bash)
export prefix=tomaskubica4

# Configure prefix (in PowerShell)
$prefix="tomaskubica4"

# Create resource group
az group create -n $prefix-onprem -l northeurope

# Create VNET
az network vnet create -n $prefix-onprem -g $prefix-onprem --address-prefix 192.168.0.0/24

# Create three subnets
az network vnet subnet create -n vpn -g $prefix-onprem --vnet-name $prefix-onprem --address-prefixes 192.168.0.0/24
```

We will now deploy Linux server that will act as VPN device.

```bash
# In bash
az storage account create -n seriakop$prefix -g $prefix-onprem

az vm create -n $prefix-vpn \
    -g $prefix-onprem \
    --image UbuntuLTS \
    --vnet-name $prefix-onprem \
    --subnet vpn \
    --size Standard_D2a_v4 \
    --admin-username labuser \
    --admin-password Azure12345678 \
    --authentication-type password \
    --zone 1 \
    --private-ip-address 192.168.0.10 \
    --public-ip-address $prefix-vpn-ip \
    --nsg "" \
    --boot-diagnostics-storage seriakop$prefix \
    --no-wait
```

```bash
# In PowerShell
az storage account create -n seriakop$prefix -g $prefix-onprem

az vm create -n $prefix-vpn `
    -g $prefix-onprem `
    --image UbuntuLTS `
    --vnet-name $prefix-onprem `
    --subnet vpn `
    --size Standard_B1s `
    --admin-username labuser `
    --admin-password Azure12345678 `
    --authentication-type password `
    --zone 1 `
    --private-ip-address 192.168.0.10 `
    --public-ip-address $prefix-vpn-ip `
    --nsg '""' `
    --boot-diagnostics-storage seriakop$prefix `
    --no-wait
```

Configure Azure side.

```bash
# In bash

# Configure onprem peer
az network vpn-site create --ip-address $(az network public-ip show -g $prefix-onprem -n $prefix-vpn-ip --query ipAddress -o tsv) \
    -n $prefix-onprem-site \
    -g $prefix-central \
    --address-prefixes 192.168.0.0/24 \
    --asn 65123 \
    --bgp-peering-address 192.168.0.10 \
    --virtual-wan $prefix-vwan
    
# Create VPN connection
az network vpn-gateway connection create -n $prefix-onprem-conn \
    -g $prefix-central \
    --gateway-name $prefix-vpn \
    --remote-vpn-site $(az network vpn-site show  -n $prefix-onprem-site -g $prefix-central --query id -o tsv) \
    --associated-route-table $(az network vhub route-table show -n defaultRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv) \
    --propagated $(az network vhub route-table show -n defaultRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv) \
    --shared-key Azure12345678 \
    --enable-bgp true 

# Capture gateway configs
## BGP AS number
az network vpn-gateway show -n $prefix-vpn -g $prefix-central --query bgpSettings.asn -o tsv

## First instance public IP 
az network vpn-gateway show -n $prefix-vpn -g $prefix-central --query bgpSettings.bgpPeeringAddresses[0].tunnelIpAddresses[0] -o tsv

## First instance BGP IP
az network vpn-gateway show -n $prefix-vpn -g $prefix-central --query bgpSettings.bgpPeeringAddresses[0].defaultBgpIpAddresses -o tsv
```


```powershell
# In PowerShell

# Configure onprem peer
az network vpn-site create --ip-address $(az network public-ip show -g $prefix-onprem -n $prefix-vpn-ip --query ipAddress -o tsv) `
    -n $prefix-onprem-site `
    -g $prefix-central `
    --address-prefixes 192.168.0.0/24 `
    --asn 65123 `
    --bgp-peering-address 192.168.0.10 `
    --virtual-wan $prefix-vwan
    
# Create VPN connection
az network vpn-gateway connection create -n $prefix-onprem-conn `
    -g $prefix-central `
    --gateway-name $prefix-vpn `
    --remote-vpn-site $(az network vpn-site show  -n $prefix-onprem-site -g $prefix-central --query id -o tsv) `
    --associated-route-table $(az network vhub route-table show -n defaultRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv) `
    --propagated $(az network vhub route-table show -n defaultRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv) `
    --shared-key Azure12345678 `
    --enable-bgp true 

# Capture gateway configs
## BGP AS number
az network vpn-gateway show -n $prefix-vpn -g $prefix-central --query bgpSettings.asn -o tsv

## First instance public IP 
az network vpn-gateway show -n $prefix-vpn -g $prefix-central --query bgpSettings.bgpPeeringAddresses[0].tunnelIpAddresses[0] -o tsv

## First instance BGP IP
az network vpn-gateway show -n $prefix-vpn -g $prefix-central --query bgpSettings.bgpPeeringAddresses[0].defaultBgpIpAddresses -o tsv
```

Configure Linux for IPSec

```bash
az serial-console connect -n $prefix-vpn -g $prefix-onprem
sudo -i
apt install quagga quagga-doc strongswan -y
export azureip=20.67.231.43   # Modify to fit yours!
export azurebgppeer=10.0.0.12   # Modify to fit yours!

cat > /etc/ipsec.conf << EOF
config setup
 
conn azure
        leftupdown=/etc/ipsec-notify.sh 
        authby=secret
        type=tunnel
        left=192.168.0.10
        leftid=$(curl ifconfig.io)
        leftsubnet=192.168.0.0/16
        right=$azureip
        rightsubnet=10.0.0.0/8
        auto=route
        keyexchange=ikev2
        leftauth=psk
        rightauth=psk
        ike=aes256-sha1-modp1024!
        ikelifetime=28800s
        aggressive=no
        esp=aes256-sha1!
        lifetime=3600s
        keylife=3600s
EOF

cat > /etc/ipsec.secrets << EOF
# In this case, we use a PSK. Format: Local.public.ip.address remote.public.ip.address : PSK 'custompresharedkey'
$(curl ifconfig.io) $azureip : PSK 'Azure12345678' 
EOF

cat > /etc/ipsec-notify.sh << EOF
#!/bin/bash
# Credit to Endre Szabó https://end.re/2015-01-06_vti-tunnel-interface-with-strongswan.html

set -o nounset
set -o errexit

VTI_IF="vti${PLUTO_UNIQUEID}"

case "${PLUTO_VERB}" in
    up-client)
        ip tunnel add "${VTI_IF}" local "${PLUTO_ME}" remote "${PLUTO_PEER}" mode vti \
            okey "${PLUTO_MARK_OUT%%/*}" ikey "${PLUTO_MARK_IN%%/*}"
        ip link set "${VTI_IF}" up
        ip route add 10.0.0.0/8 dev "${VTI_IF}"
        sysctl -w "net.ipv4.conf.${VTI_IF}.disable_policy=1"
        ;;
    down-client)
        ip tunnel del "${VTI_IF}"
        ;;
esac
EOF

ipsec restart
ipsec up azure
ping $azurebgppeer   # Ping BGP peer in Azure

# Configure BGP

cat > /etc/quagga/bgpd.conf << EOF
!
! Zebra configuration saved from vty
!   2021/10/06 05:42:41
!
hostname bgpd
password zebra
log stdout
!
router bgp 65123
 bgp router-id 192.168.0.10
 network 192.168.0.0/24
 network 192.168.1.0/24
 network 192.168.2.0/24
 network 192.168.3.0/24
 neighbor $azurebgppeer remote-as 65515
 neighbor $azurebgppeer soft-reconfiguration inbound
!
 address-family ipv6
 exit-address-family
 exit
!
line vty
!
EOF

cp /usr/share/doc/quagga-core/examples/vtysh.conf.sample /etc/quagga/vtysh.conf
cp /usr/share/doc/quagga-core/examples/zebra.conf.sample /etc/quagga/zebra.conf

systemctl enable zebra.service
systemctl enable bgpd.service
systemctl start zebra.service
systemctl start bgpd.service
systemctl status zebra.service
systemctl status bgpd.service

vtysh
show ip bgp   # You should see routes from Azure such as 10.0.0.0/16, 10.1.0.0/16, ...
```

Now we need to fix one issue. Our VPN routes are propagated to our default hub routing table. Because those are more specific our projects communicate with onprem directly, but onprem to Azure is forced throw firewall and this asymetry is not desirable. If we want traffic between onprem and Azure to go via firewall, we need to keep VPN routes in our default table (which is assiciated with firewall) so let's create another table and move our projects to it. Table into which VPN nor project propagate any routes.

```bash
# In Bash

# Check routes in Default table - it includes routes to onprem
az network vhub get-effective-routes -g $prefix-central -n $prefix-ne-hub --resource-type RouteTable -o table \
    --resource-id $(az network vhub route-table show -n defaultRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)

# Create new route table
az network vhub route-table create -n projectsRouteTable \
    --route-name all_traffic \
    -g $prefix-central \
    --vhub-name $prefix-ne-hub \
    --destination-type CIDR --destinations "0.0.0.0/0" "10.0.0.0/8" "172.16.0.0/12" "192.168.0.0/16" \
    --next-hop-type ResourceId \
    --next-hop $(az network firewall show -n $prefix-fw -g $prefix-central --query id -o tsv)

# Check routes in Projects table - it should include only routes to Azure Firewall
az network vhub get-effective-routes -g $prefix-central -n $prefix-ne-hub --resource-type RouteTable -o table \
    --resource-id $(az network vhub route-table show -n projectsRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)

# Assign new route table to project VNETs
az network vhub connection update -n project1conn -g $prefix-central --vhub-name $prefix-ne-hub \
    --associated $(az network vhub route-table show -n projectsRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)

az network vhub connection update -n project2conn -g $prefix-central --vhub-name $prefix-ne-hub \
    --associated $(az network vhub route-table show -n projectsRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)
```

```powershell
# In PowerShell

# Check routes in Default table - it includes routes to onprem
az network vhub get-effective-routes -g $prefix-central -n $prefix-ne-hub --resource-type RouteTable -o table `
    --resource-id $(az network vhub route-table show -n defaultRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)

# Create new route table
az network vhub route-table create -n projectsRouteTable `
    --route-name all_traffic `
    -g $prefix-central `
    --vhub-name $prefix-ne-hub `
    --destination-type CIDR --destinations "0.0.0.0/0" "10.0.0.0/8" "172.16.0.0/12" "192.168.0.0/16" `
    --next-hop-type ResourceId `
    --next-hop $(az network firewall show -n $prefix-fw -g $prefix-central --query id -o tsv)

# Check routes in Projects table - it should include only routes to Azure Firewall
az network vhub get-effective-routes -g $prefix-central -n $prefix-ne-hub --resource-type RouteTable -o table `
    --resource-id $(az network vhub route-table show -n projectsRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)

# Assign new route table to project VNETs
az network vhub connection update -n project1conn -g $prefix-central --vhub-name $prefix-ne-hub `
    --associated $(az network vhub route-table show -n projectsRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)

az network vhub connection update -n project2conn -g $prefix-central --vhub-name $prefix-ne-hub `
    --associated $(az network vhub route-table show -n projectsRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv)
```

You can now add firewall rules, for example to access web balancer (10.1.1.100) from your "onprem" machine.

Congratulations! This is end of our lab.