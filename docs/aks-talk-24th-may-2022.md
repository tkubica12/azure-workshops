# AKS structure and tenancy strategy
- AKS vs. ITS Managed AKS product
- Resource isolation - what is shared and how much you care
  - Cluster-level components such as CRDs
  - VT-X compute isolation using node pools
  - Kernel isolation might not be enough for multi-tenancy
    eg. resource limits on CPU, memory, process count, but what about fswatchers etc.?
  - Leverage node/pod affinity and anti-affinity to achieve your goals
  - Networking! Mind classified/unclassified concepts vs. zero trust vs. how ITS managed AKS overcame this
- GitOps using Flux and/or Argo CD
  - DRY - Do Not Repeat Yourself -> see [https://github.com/tomas-iac/common-kubernetes](https://github.com/tomas-iac/common-kubernetes)
    - Option 1: Use Kustomize bases for project and overlays for environments or even instances such as regions (2nd level of patching) using folders
    - Option 2: Package your project as product in Helm chart and declare abstractions (interfaces) and use separate values files per environment (typically i per-environment folders)
  - Model process around Git features (PRs, reviews, discussions, issues, tasks, approvals)
  - How about cloud services such as DBs and queues?
    - Always prefer PaaS options -> you get better service and (most importantly) SLA !
    - If you want to be cool look at Azure Service Operator or Crossplane with GitOps pull-based model
    - If you want to be rock solid and support everything use Terraform, Bicep or Pulumi
      You should still use Git as source of truth and process! You will probably just rather push than pull,
      but that can still count as GitOps.

# AKS and FinOps
- Kubecost
- FinOps strategy
  - Reserve whatever runs >8h a day on average (3y commit discount is better than PAYG with its complexity)
  - Use autoscaler or pre-scale before event (campaign etc.)
  - Use KEDA to scale on rich metrics (and potentially scale to zero)
  - Consider serverless platforms if you really need scale quickly! 
    Azure Container Apps, Azure Functions
  - Size your nodes well, use nodepools and affinity
    - Too small equals too much overhead (eg. 4GB RAM is not good idea)
    - Too big equals less scalining granularity (eg. 768GB is often underutilized) and more impact on upgrades/failures
    - Choose right CPU:RAM ratio (F 1/2 -> D 1/4 -> E 1/8 -> M 1/>8)

# AKS - building highly available apps

## Concepts

### Tolerate vs. avoid failures
- Scale-out rather than scale-up 
  - Always set requests/limits for scheduler to work properly
  - Use cluster autoscaler if you need dynamic scale
  - Consider alternatives such as extreem scale-out with serverless (Azure Functions)
- Chaos engineering
  - Use Chaos Mesh in AKS together with Azure Chaos Studio (preview)
  - Chaos engineering vs. DR drill
  
### Site Reliability Engineering
- SLOs, SLAs
- KPIs and metrics
- Error budget - get punished for over-delivering SLAs 
- PaaS vs. IaaS and composite SLA

### Safe deployment practices
- Progressive delivery (requires good metrics)
- Infra canary (Flagger, Argo Rollouts) vs. feature toggles 
  (eg. with Azure App Configuration Service)
- A/B testing
- Green/Blue deployment
- GitOps - Git as source of truth

### Immutability
- Immutable infrastructure (phoenix servers)
  - Docker images
  - Pet vs. Cattle
- Immutable storage (append only)
  - CQRS and event sourcing (see later)
  - Blockchain
  - Eventing and time-series
  - Append optimized with garbage collection
- Functional vs. actor vs. object-oriented

### Automation
- Declarative whenever possible
- Imperative as glue between systems (eg. CI/CD)
- Reconciliation loop - pull vs. push based approaches 
  
## Layers

### Cloud physical layer
- No SPOF in datacenter
- DCs grouped to Avalaiability Zones within region, <2ms appart
- Regions and control plane safe deployment processes
- Global WAN, DDoS, DNS, Auth infrastructure
- Edge zones
- [https://infrastructuremap.microsoft.com/explore](https://infrastructuremap.microsoft.com/explore)
- [https://natick.research.microsoft.com/](https://natick.research.microsoft.com/)
- [https://status.azure.com/](https://status.azure.com/)

### Global user access, security and API          
- Distributed WAF with DDoS and anycast (eg. Azure Front Door)
- In-region L7 or L4 balancers
- DNS-based solutions are becoming less popular
- Use single global IdP to integrate all scenarios 
  (AAD with External Identities such as legacy, Google, Facebook)
- Use proper API Management layer
  - Streamline security and style
  - Enhance internal, B2B and B2C innovation
  - Enable evolutionary design with facade pattern

### Stateless layer
- Distribute control plane between AZs, use management plane between regions 
  - AKS clusters spread AZs, but different cluster in each region 
  - GitOps as management plane
  - edge routing eg. with Front Door
  - service discovery eg. with DNS or Consul
- Images, secrets, Git or authentication services replicated across regions
- Static content
  - use CDN, storage or dedicated service (Azure Static WebApps)
  - avoid traditional compute (eg. via container)
- Use async as much as possible
- Consider serverless and rapid scaling
- Prefer high-level platforms whenever possible 
  to speed-up innovation and time-to-market
  (eg. Azure Container Apps vs. Azure Kubernetes Service)

### Stateful layer
- PACELC design choices
  - Strong consistency (latency, cost)
  - Eventual consistency (performance)
  - Optimistic concurrency control and multi-write
  - In-between (session, bounded staleness, consistent prefix)
  - [https://docs.microsoft.com/en-us/azure/cosmos-db/consistency-levels](https://docs.microsoft.com/en-us/azure/cosmos-db/consistency-levels)
  - "Starbucks does not use 2 phase commit"
    overbooking problem and business solutions to it vs. technical ones
- Shared everything vs. shared nothing vs. shared storage
- AKS data persistency options
  - Always choice No1 -> let Microsoft do this for use, use PaaS!
  - LRS disks (single zone) -> for HA use only with shared-nothing architecture (eg. Kafka, Cassandra etc.)
  - ZRS disks or ZRS Azure Files -> "cheap HA" for hard recovery in different zone
  - Multi-attach ZRS disks (IO fencing) -> proper shared-storage HA (low level implementation, bring your own clustered FS)
  - Shared ZRS Azure Files -> proper shared-storage HA (higher level implementation, need to support CIFS or NFS)
  - Local very fast NVMe SSDs -> extreme performance with shared-nothing architecture
    (not recommended unless you really know what you are doing - storage is lost with every single cluster upgrade!)
- AKS and PACELC
  - Deployment object is not guarantee! "at least 1 replica" is not the same as exactly 1 replica, dataloss if not handled properly
  - Use StatefulSets if you need guarantees (consistent naming, consistent order of creation etc.), 
    but beware availability implications (long recovery time for singleton due to consistency guarantee, 
    might require manual action, always use multiple replicas)
- Cloud services should be you first choice
  - IaaS: 99,99% * my management and software even with 99,99% = 99,98% composite
  - PaaS: SQL DB BC = 99,995%
- CQRS
- Event sourcing vs. CRUD
  - Use change feeds to implement async fan-out (eg. CosmosDB)
  - Business events (eg. order created) may decouple logic from data implementation
- Transaction consistency
  - ACID in database
  - Saga pattern and compensation transactions
  - Eventual consistency with business compensation process
- RTO and RPO

