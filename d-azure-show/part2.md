# Basics of Azure administration

## How can I connect and manage access for my team?
- Authn -> MFA, conditional access, SSO
- Authz -> who (AAD user, group, managed identity, SP), what on what scope

## Should I use GUI? CLI? What are best practices?
### Walk throw GUI
### CLI demo
  
```bash
az group list -o table

az group create -n bashdemo -l westeurope
for i in {1..5}; do
    az disk create -n bashdisk$i -g bashdemo --size-gb 10 --sku Standard_LRS
done

az disk list -g bashdemo --query [].name -o tsv | xargs -I {} az disk update -n {} -g bashdemo --sku Premium_LRS

az group delete -n bashdemo -y
```

### PowerShell demo

```powershell
Get-AzResourceGroup

New-AzResourceGroup -Name pwshdemo -Location westeurope
for ($i = 1 ; $i -le 5 ; $i++)
{ 
    $diskConfig = New-AzDiskConfig -Location westeurope -CreateOption Empty -DiskSizeGB 10 -SkuName "Standard_LRS"
    New-AzDisk -DiskName pwshdisk$i -Disk $diskConfig -ResourceGroupName pwshdemo
}

ForEach ($disk in Get-AzDisk -ResourceGroupName pwshdemo)
{
    $diskUpdateConfig = New-AzDiskUpdateConfig -SkuName "Premium_LRS"
    Update-AzDisk  -DiskName $disk.Name -DiskUpdate $diskUpdateConfig -ResourceGroupName  $disk.ResourceGroupName
}

Remove-AzResourceGroup -Name pwshdemo -Force
```

### Bicep demo
```
// Storage account
resource myStorage 'Microsoft.Storage/storageAccounts@2021-09-01' = {
  name: uniqueString(resourceGroup().id)
  location: 'westeurope'
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}

// Output message
output message string = 'My storage account name is ${myStorage.name}'

// Output storage fqdn
output storageFqdn string = myStorage.properties.primaryEndpoints.blob
```

```bash
az group create -n iac -l westeurope
az bicep build -f demo.bicep
az deployment group create -g iac --template-file demo.json
az group delete -n iac -n --no-wait
```

## How can I organize resources and keep track of costs?
- Explain subscriptions and resource groups
- Explain tags and enforcement via policy
- Show cost management
- Explain budgets - actual vs. forecasted, scope, filters, automation (ticket, Teams message, killing resources)
 

# Azure Services

## What services are available?
https://azure.microsoft.com/en-gb/services/

## When should I use IaaS vs. PaaS vs. SaaS?
https://azure.microsoft.com/en-us/overview/types-of-cloud-computing/

## Can I leverage existing licensing for cloud?
https://azure.microsoft.com/en-gb/pricing/hybrid-benefit/#calculator
https://azure.microsoft.com/en-us/pricing/details/virtual-machines/red-hat/

## Where can I find pricing information and SLAs for each service?
https://azure.microsoft.com/en-us/pricing/calculator/

## Where can I find SLAs for each service?
https://azure.microsoft.com/en-us/support/legal/sla/
 

# Tools and resources

## Cloud Adoption Framework
https://azure.microsoft.com/en-us/overview/cloud-enablement/cloud-adoption-framework/

## Well-architected
https://docs.microsoft.com/en-us/azure/architecture/framework/

## Architecture center
https://docs.microsoft.com/en-us/azure/architecture/

## Documentation
https://docs.microsoft.com/en-us/azure/?product=popular

## Visual Studio Code addons