# DR between Azure regions with Azure Site Recovery
This demo showcase VM replication from one region to another in enterprise-grade network with forced tunneling, private endpoints, hub-and-spoke topology, and Azure Firewall.

1. Deploy
2. Explain scenario, components, communication flows
3. Showcase failover - explain various recovery point options (minimize RTO, minimize RPO, maxime app-level consistency)
4. Explain how to failback

ZRS example

```bash
# Get OS disk id
disk=$(az vm show -n win-vm3 -g d-asr-zrs --query storageProfile.osDisk.managedDisk.id -o tsv)

# Destroy VM in zone 1 to simulate failure
az vm delete -n win-vm3 -g d-asr-zrs -y --force-deletion true

# Get subnet id
subnet=$(az network vnet subnet show --vnet-name primary-spoke1 -n default -g d-asr-primary --query id -o tsv)

# Create VM by attaching existing managed disks as OS
az vm create -n win-vm3 -g d-asr-zrs --attach-os-disk $disk --os-type Windows --zone 2 --subnet $subnet --public-ip-address ""
```