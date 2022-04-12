# 07 - Publishing apps via L7 Web Application Firewall
We do not want to expose applications to Internet directly via DNAT - let's deploy Web Application Firewall in DMZ and publish our app.

Let's create new DMZ network, attach it to vWAN hub and configure Azure Firewall to allow access from DMZ to all projects via ports 80 and 443. As we will deploy WAF with public IP in this network we will place it to different routing table so it has direct access to Internet and only communication to other projects go via Azure Firewall.

```bash
# Configure prefix (in bash)
export prefix=tomaskubica4

# Configure prefix (in PowerShell)
$prefix="tomaskubica4"

# Create resource group
az group create -n $prefix-dmz -l northeurope

# Create VNET
az network vnet create -n $prefix-dmz -g $prefix-dmz --address-prefix 10.253.0.0/16

# Create subnet
az network vnet subnet create -n machines -g $prefix-dmz --vnet-name $prefix-dmz --address-prefixes 10.253.0.0/24
az network vnet subnet create -n waf -g $prefix-dmz --vnet-name $prefix-dmz --address-prefixes 10.253.1.0/24
```

Create route table, connect DMZ to hub and configure rules on Azure Firewall

```bash
# In Bash

# Create route table
az network vhub route-table create -n dmzRouteTable \
    --route-name internal_traffic \
    -g $prefix-central \
    --vhub-name $prefix-ne-hub \
    --destination-type CIDR --destinations "10.0.0.0/8" "172.16.0.0/12" "192.168.0.0/16" \
    --next-hop-type ResourceId \
    --next-hop $(az network firewall show -n $prefix-fw -g $prefix-central --query id -o tsv)

# Connect DMZ to hub
az network vhub connection create -n dmzconn \
    -g $prefix-central \
    --vhub-name $prefix-ne-hub \
    --remote-vnet $(az network vnet show -n $prefix-dmz -g $prefix-dmz --query id -o tsv) \
    --associated $(az network vhub route-table show -n dmzRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv) \
    --propagated $(az network vhub route-table show -n noneRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv) \
    --labels ""

# Add firewall rule
az network firewall policy rule-collection-group collection add-filter-collection --name waf \
    --rule-collection-group-name commonInternal \
    --rule-name web \
    --rule-type NetworkRule \
    --policy-name $prefix-fw-policy \
    --resource-group $prefix-central \
    --description "Allow SSH from jump to specific VM" \
    --source-addresses "10.253.0.0/16" \
    --destination-addresses "10.0.0.0/8" \
    --destination-ports 80 443 \
    --ip-protocols TCP \
    --action Allow \
    --collection-priority 190
```

```powershell
# In PowerShell

# Create route table
az network vhub route-table create -n dmzRouteTable `
    --route-name internal_traffic `
    -g $prefix-central `
    --vhub-name $prefix-ne-hub `
    --destination-type CIDR --destinations "10.0.0.0/8" "172.16.0.0/12" "192.168.0.0/16" `
    --next-hop-type ResourceId `
    --next-hop $(az network firewall show -n $prefix-fw -g $prefix-central --query id -o tsv)

# Connect DMZ to hub
az network vhub connection create -n dmzconn `
    -g $prefix-central `
    --vhub-name $prefix-ne-hub `
    --remote-vnet $(az network vnet show -n $prefix-dmz -g $prefix-dmz --query id -o tsv) `
    --associated $(az network vhub route-table show -n dmzRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv) `
    --propagated $(az network vhub route-table show -n noneRouteTable -g $prefix-central --vhub-name $prefix-ne-hub --query id -o tsv) `
    --labels '""'

# Add firewall rule
az network firewall policy rule-collection-group collection add-filter-collection --name waf `
    --rule-collection-group-name commonInternal `
    --rule-name web `
    --rule-type NetworkRule `
    --policy-name $prefix-fw-policy `
    --resource-group $prefix-central `
    --description "Allow SSH from jump to specific VM" `
    --source-addresses "10.253.0.0/16" `
    --destination-addresses "10.0.0.0/8" `
    --destination-ports 80 443 `
    --ip-protocols TCP `
    --action Allow `
    --collection-priority 190
```

We will now deploy Azure Application Gateway with Web Application Firewall to our DMZ and configure it to expose our web application from project1.

```bash
# In Bash

# Create zone-redundant public ip
az network public-ip create -n $prefix-waf-ip -g $prefix-dmz --sku Standard --zone 1 2 3

# Create Application Gateway WAF
az network application-gateway create -n $prefix-waf \
    -g $prefix-dmz \
    --min-capacity 2 \
    --max-capacity 5 \
    --zones 1 2 3 \
    --frontend-port 80 \
    --http-settings-port 80 \
    --http-settings-protocol Http \
    --http2 Enabled \
    --sku WAF_v2 \
    --servers 10.1.1.100 \
    --public-ip-address $prefix-waf-ip \
    --subnet waf \
    --vnet-name $prefix-dmz
```

```powershell
# In PowerShell

# Create zone-redundant public ip
az network public-ip create -n $prefix-waf-ip -g $prefix-dmz --sku Standard --zone 1 2 3

# Create Application Gateway WAF
az network application-gateway create -n $prefix-waf `
    -g $prefix-dmz `
    --min-capacity 2 `
    --max-capacity 5 `
    --zones 1 2 3 `
    --frontend-port 80 `
    --http-settings-port 80 `
    --http-settings-protocol Http `
    --http2 Enabled `
    --sku WAF_v2 `
    --servers 10.1.1.100 `
    --public-ip-address $prefix-waf-ip `
    --subnet waf `
    --vnet-name $prefix-dmz
```

Test you can access app over Internet.

```bash
curl $(az network public-ip show -n $prefix-waf-ip -g $prefix-dmz --query ipAddress -o tsv)
```