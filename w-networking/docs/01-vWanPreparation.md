## 01 - vWAN preparation
In this step we will open separate window to start deployment of Azure Virtual WAN, because it takes quite some time so it is ready for us later in the lab, when we need it. Creating hub will tike about 10 minutes, creating firewall about 20 minutes. Meanwhile we will continue with different tasks. Please start deploying now.

```bash
# Configure prefix (in bash)
export prefix=tomaskubica4

# Configure prefix (in PowerShell)
$prefix="tomaskubica4"

# Create resource group
az group create -n $prefix-central -l northeurope

# Create vWAN
az network vwan create -n $prefix-vwan -g $prefix-central --type Standard

# Create Hub
az network vhub create -n $prefix-ne-hub -g $prefix-central --vwan $prefix-vwan --address-prefix 10.0.0.0/16 --sku Standard

# Create empty firewall policy
az network firewall policy create -n $prefix-fw-policy -g $prefix-central --sku Premium

# Create firewall
az network firewall create -n $prefix-fw -g $prefix-central --vhub $prefix-ne-hub --public-ip-count 1 --tier Premium --sku AZFW_Hub --firewall-policy $prefix-fw-policy --no-wait

# Create VPN gateway
az network vpn-gateway create -n $prefix-vpn -g $prefix-central --vhub $prefix-ne-hub --no-wait
```