# Azure Network Monitoring demo
This demo shows common monitoring tasks on networking and basic connectivity in Azure:
- Connection Monitor to measure connection, latency and packet loss between locations and towards common services
- Traffic analytics
- NVA base monitoring (CPU, IO, packets)
- NVA planned maintenance
- Alerting and integration with other systems

# Deployment
In default.auto.tfvars configure existing Network Watcher instances if you have any in your subscription. There can be just one instance per region per subscription. If you do not have any in your subscription you can leave it blank and template will create one for you.

Also you can modify two locations used for template - use form without whitespace such as eastus2, westeurope, northeurope etc.

To deploy template run:
```bash
cd terraform
terraform init
terraform apply -auto-approve
```

In order for Logic App to work got to myteams connector in Azure Portal and click on Authorize so connector gets token to Teams.

# Scenario deployed
- 2 VNETs in different regions peered to each other
- VM in every VNET with Network Watcher agent installed
- Monitoring resources such as Log Analytics workspace and storage accounts
- NSG configured on each subnet and network flow logs enabled, stored in storage and Log Analytics and analyzed with Traffic Analytics
- Connection Monitor configured between two VMs
- Connection Monitor towards SaaS services configured
- Resource monitoring for VMs (agent-less, similar to what would be available on NVA that is locked for installing Azure agents)
- Alert for resource health on NVA
- Alert for metric on NVA
- Alert action - send email
- Alert action - webhook
- Alert for connection failure
- Logic App
- Alert action - run Logic App with complex behavior
  
# About planned maintenance
Patching requiring reboot -> you will be notified, often you will get option to initiate reboot when it is convenient for you

Patching not requiring reboot (few seconds pause):
- You are not notified from outside of VM nor have ability to select your time
- You can receive this information using Scheduled Event from inside of VM
- If you can run custom script in your NVA you can react on planned pause(15 minutes notice) - eg. failover to other NVA

General recommendation: most pause events are less than 10 seconds and it is usually better to not do anything. For encryption clock might be important so make sure you configure time-sync properly (use host-based solution, not remote NTP server as host-based gets corrected much quicker after VM unpaused).

# Docs
- [Resource Health Events](https://learn.microsoft.com/en-us/azure/service-health/resource-health-vm-annotation)
- [VM maintenance](https://learn.microsoft.com/en-us/azure/virtual-machines/maintenance-and-updates)
- [Scheduled Events](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/scheduled-events)
- [Time-sync](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/time-sync)