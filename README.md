# Azure technical hands-on workshops and demos
This repo contains materials I am using with customers to help them learn Azure, AI, operations, security and development practices when using cloud.

## How to clone this repository

To clone this repository along with all submodules, use the following command:

```sh
git clone --recurse-submodules https://github.com/tkubica12/azure-workshops.git
```

If you have already cloned the repository without submodules, you can initialize and update them with:

```sh
git submodule update --init --recursive
```

# Demos
Each d-topic folder contains repeatable demo and sometimes link to talk markmap.

## AI demos
- [4 approaches to sentiment analysis - llm, finetuning, encoder, embeddings with classifier](https://github.com/tkubica12/d-ai-sentiment)
- [LLM learning tool - Token Visualizer](https://github.com/tkubica12/d-ai-token-visualizer)
- [Scalable AI chat](https://github.com/tkubica12/scalable-ai-chat/)
- [Async pattern in AI apps](./d-ai-async/)
- [AI Inference SDK with monitoring](./d-ai-inference-sdk-with-monitoring/)
- [Advanced RAG patterns](./d-ai-rag/)
- [Browser Use Agent](./d-ai-browser-use/)
- [Lang Graph multi-agent system with UI, OpenTelemetry, Azure Monitor and Container Apps](./d-ai-langgraph-aca-azmonitor/)
- [AI reasoning with tools](./d-ai-reasoning-with-tools/)
- [From prompt to thinking to tool use](./d-ai-prompt-think-tool/)
- [Dynamic AI-generated UI](./d-ai-dynamic-ui/)

## Azure Kubernetes Service demos
- [Operators](./d-aks-operators/)
- [Private Link Service eg. in SaaS provider scenario](./d-aks-privatelinkservice/)
- [Workload Federated Identity using User Managed Identity, Terraform and Key Vault](./d-aks-federated-identity/)
- [Kata containers for strict isolation](./d-aks-kata/)
- [Secrets - notes and tips](./d-aks-secrets/)
- [Azure Kubernetes Fleet Manager](./d-kubernetes-fleet/../)
- [Cost management](./d-aks-cost-management/)
- [ARM64 CPUs - AKS, Terraform, GitHub Actions and multi-arch images in ACR](./d-aks-arm64/)
- [Microsoft Defender for Containers](./d-aks-defender/)
- [ChaosMesh](./d-aks-chaosmesh/)
- [AKS with ArcoCD and Argo Rollouts](./d-aks-argo-cd-and-rollouts/)
- [Istio addon with Prometheus and Grafana](./d-aks-istio/)
- [Azure Container Storage](./d-aks-azurecontainerstorage/)
- [AKS Advanced Container Networking Services](./d-aks-acns/)
- [AKS Static Egress Gateway](./d-aks-static-egress-gw/)
- [AKS Isolated](./d-aks-network-isolated/)
- [AKS Node Autoprovisioning](./d-aks-karpenter/)
  
## Other demos
- [Azure Managed Redis](./d-azure-managed-redis/)
- [Azure API Management](./d-api-management/)
- [Azure API Management in AKS](./d-apim-in-aks/)
- [Azure private DNS resolver](./d-dns-resolver/)
- [Azure Chaos Studio demo](./d-chaos-studio/)
- [Microsoft Dev Center - DevBox and Deployment Environments](./d-dev-ex/)
- [Azure Managed Prometheus and Grafana](./d-managed-prometheus/)
- [Data encryption, security and confidential computing](./d-data-security/)
- [DR between Azure regions with Azure Site Recovery](./d-asr/)
- [Azure Network Monitoring](./d-net-monitor/)
- [Azure Dedicated Hosts](./d-dedicated-hosts/)
- [Azure ML](https://github.com/tkubica12/ai-demos/tree/main/azureml)
- [Azure OpenAI Service](https://github.com/tkubica12/ai-demos/tree/main/openai) 
- [Azure Files with AD integration](./d-storage-files-ad/)
- [Azure Disk shared with SCSI PR](./d-storage-disk-shared/) 
- [Azure Blob storage demo](./d-azure-blob-storage/)
- [Azure Container Apps](./d-aca/)
- [DR solution for regions with small paired regions such as Germany West Central](./d-gwc-dr/)
- [Application Gateway with cert in Key Vault](./d-appgw-kv/)
- [Azure Container Apps sessions with LLM and LangChain](./d-aca-sessions/)

# Workshops
Each w-topic folder contains following sections:
- README.md with intro and links
- docs with individual lessons/tasks
- resources with files and artefacts used during workshop
- challenge contains your challenge to work on after workshop
  
List of workshops:
- [Introduction to Azure](./w-azure-basics/)
- [Introduction to Azure Kubernetes Service](./w-aks-intro/)
- [Introduction to storage in Azure](./w-storage/)
- [Introduction to networking in Azure](./w-networking/)
- [Terraform on Azure](./w-terraform-on-azure/)