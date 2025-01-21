# AKS Static Egress Gateway
Deploy solution using terraform and note gateway subnet. In kubernetes folder deploy multiple GW configurations and Pods annotated to use those for egress traffic. Show CRD for Staticgatewayconfigurations to see how each allocates secondary private IPs from both gateway nodes (for redundancy). You might to MC group, find VMSS and show its NIC containing those IPs.

Solution can also automatically allocate Public IP range and assign addresses to gateways.