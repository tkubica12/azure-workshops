# 06 - Configuring Azure Firewall
Traffic between projects and to outside world is going through Azure Firewall now. Let's configure some rules to allow wanted traffic.

First we will focus on outbound to Internet controls using L7 features (transparent proxy). In previous lab we have proven we are not able to access site http://ifconfig.io/all. Let's now add rules to allow this.

```bash
# In Bash

# Create rule collection group commonAppOutbound
az network firewall policy rule-collection-group create --name commonAppOutbound \
    --policy-name $prefix-fw-policy \
    --resource-group $prefix-central \
    --priority 200

# Create rule for ifconfig.io and similar tools in new collection toolsSites under commonAppOutbound
az network firewall policy rule-collection-group collection add-filter-collection --name toolsSites \
    --rule-collection-group-name commonAppOutbound \
    --rule-name ifconfig \
    --rule-type ApplicationRule \
    --policy-name $prefix-fw-policy \
    --resource-group $prefix-central \
    --protocols "Http=80" "Https=443"\
    --description "Allow ifconfig-like tools" \
    --source-addresses "*" \
    --target-fqdns "ifconfig.io" "ifconfig.me" \
    --action Allow \
    --collection-priority 200

# Add additional rule to toolsSites collection under commonAppOutbound collection group
az network firewall policy rule-collection-group collection rule add --name myip \
    --rule-collection-group-name commonAppOutbound \
    --collection-name toolsSites \
    --rule-type ApplicationRule \
    --policy-name $prefix-fw-policy \
    --resource-group $prefix-central \
    --protocols "Https=443"\
    --description "Allow myip tools" \
    --source-addresses "*" \
    --target-fqdns "*.my-ip.io" "my-ip.io"

# Create new collection updateServices under commonAppOutbound collection group for Ubuntu
az network firewall policy rule-collection-group collection add-filter-collection --name updateServices \
    --rule-collection-group-name commonAppOutbound \
    --rule-name ubuntu \
    --rule-type ApplicationRule \
    --policy-name $prefix-fw-policy \
    --resource-group $prefix-central \
    --protocols "Http=80" "Https=443"\
    --description "Allow Ubuntu update services" \
    --source-addresses "*" \
    --target-fqdns "ubuntu.com" "*.ubuntu.com" "packages.microsoft.com" \
    --action Allow \
    --collection-priority 210

# Add update services for Windows using predefined FQDN tag
az network firewall policy rule-collection-group collection rule add --name windowsUpdate \
    --rule-collection-group-name commonAppOutbound \
    --collection-name updateServices \
    --rule-type ApplicationRule \
    --policy-name $prefix-fw-policy \
    --resource-group $prefix-central \
    --protocols "Https=443"\
    --description "Allow WIndows update services" \
    --source-addresses "*" \
    --fqdn-tags "WindowsUpdate"
```

```powershell
# In PowerShell

# Create rule collection group commonAppOutbound
az network firewall policy rule-collection-group create --name commonAppOutbound `
    --policy-name $prefix-fw-policy `
    --resource-group $prefix-central `
    --priority 200

# Create rule for ifconfig.io and similar tools in new collection toolsSites under commonAppOutbound
az network firewall policy rule-collection-group collection add-filter-collection --name toolsSites `
    --rule-collection-group-name commonAppOutbound `
    --rule-name ifconfig `
    --rule-type ApplicationRule `
    --policy-name $prefix-fw-policy `
    --resource-group $prefix-central `
    --protocols "Http=80" "Https=443" `
    --description "Allow ifconfig-like tools" `
    --source-addresses "*" `
    --target-fqdns "ifconfig.io" "ifconfig.me" `
    --action Allow `
    --collection-priority 200

# Add additional rule to toolsSites collection under commonAppOutbound collection group
az network firewall policy rule-collection-group collection rule add --name myip `
    --rule-collection-group-name commonAppOutbound `
    --collection-name toolsSites `
    --rule-type ApplicationRule `
    --policy-name $prefix-fw-policy `
    --resource-group $prefix-central `
    --protocols "Https=443" `
    --description "Allow myip tools" `
    --source-addresses "*" `
    --target-fqdns "*.my-ip.io" "my-ip.io"

# Create new collection updateServices under commonAppOutbound collection group for Ubuntu
az network firewall policy rule-collection-group collection add-filter-collection --name updateServices `
    --rule-collection-group-name commonAppOutbound `
    --rule-name ubuntu `
    --rule-type ApplicationRule `
    --policy-name $prefix-fw-policy `
    --resource-group $prefix-central `
    --protocols "Http=80" "Https=443"`
    --description "Allow Ubuntu update services" `
    --source-addresses "*" `
    --target-fqdns "ubuntu.com" "*.ubuntu.com" "packages.microsoft.com" `
    --action Allow `
    --collection-priority 210

# Add update services for Windows using predefined FQDN tag
az network firewall policy rule-collection-group collection rule add --name windowsUpdate `
    --rule-collection-group-name commonAppOutbound `
    --collection-name updateServices `
    --rule-type ApplicationRule `
    --policy-name $prefix-fw-policy `
    --resource-group $prefix-central `
    --protocols "Https=443" `
    --description "Allow WIndows update services" `
    --source-addresses "*" `
    --fqdn-tags "WindowsUpdate"
```

Test it.

```bash
az serial-console connect -n $prefix-vm -g $prefix-project2
curl http://ifconfig.io/all
    sudo apt update
```

Go to Azure Portal and investigate other options in policy like URLs, TLS inspection, IPS it Web categorization.

As next step we will now allow jump server in project1 to access servers in project2 via SSH.

```bash
# In Bash

# Let's create few IP groups so we can reference it in rules
az network ip-group create -n $prefix-project1 -g $prefix-central --ip-addresses 10.1.0.0/16 
az network ip-group create -n $prefix-project2 -g $prefix-central --ip-addresses 10.2.0.0/16 
az network ip-group create -n $prefix-jump-project1 -g $prefix-central --ip-addresses 10.1.0.0/24

# Create rule collection group commonInternal
az network firewall policy rule-collection-group create --name commonInternal \
    --policy-name $prefix-fw-policy \
    --resource-group $prefix-central \
    --priority 250

# Allow SSH
az network firewall policy rule-collection-group collection add-filter-collection --name management \
    --rule-collection-group-name commonInternal \
    --rule-name SSH \
    --rule-type NetworkRule \
    --policy-name $prefix-fw-policy \
    --resource-group $prefix-central \
    --description "Allow SSH from jump to specific VM" \
    --source-ip-groups $prefix-jump-project1 \
    --destination-ip-groups $prefix-project2  \
    --destination-ports 22 \
    --ip-protocols TCP \
    --action Allow \
    --collection-priority 200
```

```powershell
# In PowerShell

# Let's create few IP groups so we can reference it in rules
az network ip-group create -n $prefix-project1 -g $prefix-central --ip-addresses 10.1.0.0/16 
az network ip-group create -n $prefix-project2 -g $prefix-central --ip-addresses 10.2.0.0/16 
az network ip-group create -n $prefix-jump-project1 -g $prefix-central --ip-addresses 10.1.0.0/24

# Create rule collection group commonInternal
az network firewall policy rule-collection-group create --name commonInternal `
    --policy-name $prefix-fw-policy `
    --resource-group $prefix-central `
    --priority 250

# Allow SSH
az network firewall policy rule-collection-group collection add-filter-collection --name management `
    --rule-collection-group-name commonInternal `
    --rule-name SSH `
    --rule-type NetworkRule `
    --policy-name $prefix-fw-policy `
    --resource-group $prefix-central `
    --description "Allow SSH from jump to specific VM" `
    --source-ip-groups $prefix-jump-project1 `
    --destination-ip-groups $prefix-project2  `
    --destination-ports 22 `
    --ip-protocols TCP `
    --action Allow `
    --collection-priority 200
```

```bash
az serial-console connect -n $prefix-vm -g $prefix-project2
export prefix=tomaskubica4
ssh $prefix-vm.$prefix.cz
```