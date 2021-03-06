# Networking intro

## 00 - Preparation and tooling
Please make sure that you as participant is ready! Also as organizer make sure environment is prepared and everyone is up to speed.

[guide](docs/00-PreparationAndTooling.md)

## 01 - Preparation steps for Azure Virtual WAN
In this step we will open separate window to start deployment of Azure Virtual WAN, because it takes quite some time so it is ready for us later in the lab, when we need it. Creating hub will tike about 10 minutes, creating firewall about 20 minutes. Meanwhile we will continue with different tasks. Please start deploying now.

[guide](docs/01-vWanPreparation.md)

## 02 - Basic virtual network
In this lab we will create virtual network with subnets, deploy virtual machines and test connectivity.

[guide](docs/02-basicVirtualNetwork.md)

## 03 - Segmentation with network security groups
We will use central firewall between projects and environments, but within project we want to deploy something simple and cheap to enable microsegmentation.

[guide](docs/03-NSGs.md)

## 04 - Using standard L4 Azure Load Balancers
Let's deploy web application to our servers and use Azure LB to load balance traffic.

[guide](docs/04-loadBalancer.md)

## 05 - Central connectivity and controls with Azure vWAN and Azure Firewall
Now we will connect this project to overall enterprise network topology with centralized network controls on Azure Firewall vis Azure Virtual WAN.

[guide](docs/05-vWanSecuredHub.md)

## 06 - Configuring Azure Firewall
Traffic between projects and to outside world is going through Azure Firewall now. Let's configure some rules to allow wanted traffic.

[guide](docs/06-AzureFirewall.md)

## 07 - Publishing apps via L7 Web Application Firewall
We do not want to expose applications to Internet directly via DNAT - let's deploy Web Application Firewall in DMZ and publish our app.

[guide](docs/07-WAF.md)

## 08 - Using managed services mapped to internal network via Private Endpoint
Applications will likely use managed services - let's make those mapped to internal network via Private Endpoint.

[guide](docs/08-PrivateEndpoint.md)

## 09 - Bring your own hybrid DNS services
In next step we will deploy shared resources such as custom DNS server for conditional forwarding to on-premises and configure hybrid DNS infrastructure.

[guide](docs/09-hybridDns.md)

## 10 - Connect on-premises networks
In last step we will use VPN to setup connection to on-premises networks.

[guide](docs/10-onpremNetwork.md)

## Clean up
[guide](docs/99-cleanUp.md)

Where to go from here? 
- Automate everything with Infrastructure as Code such as Terraform or Bicep
- Investigate other network services such as Azure Front Door, Azure Global Load Balancer, usage of 3rd party NVAs with Route Server, Express Route, etc.
- Investigate redundancy options for global connectivity
- Implement governance and monitoring
- Integrate security solutions such as SIEM (eg. Microsoft Sentinel)


To clean up follow [here](docs/99-cleanUp.md)