# AKS Isolated
This demo showcase AKS cluster in fully isolated environment with no outbound internet access.

Deploy demo using Terraform. Then use Bastion to access client VM, log in and use browser to look at Azure Portal. Showcase internal ACR with replicas of AKS required images and caching rules there. 