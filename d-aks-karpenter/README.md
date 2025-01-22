# AKS Node Auto Provisioning with Karpenter
Use Terraform to deploy AKS cluster with Karpenter enabled.

Deploy ```nodepools.yaml``` which will create 3 alternative pool options with different CPU:RAM ratios.

Deploy ```high-cpu.yaml``` which will create a pods with high CPU requirements, but low memory needs. See how Karpenter chooses F series nodes.

Deploy ```high-memory.yaml``` which will create a pods with high memory requirements, but low CPU needs. See how Karpenter chooses E series nodes.