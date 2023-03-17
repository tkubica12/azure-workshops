# [Highly available cloud native apps in cloud](https://learn.microsoft.com/en-us/azure/architecture/)


## Concepts

### Tolerate vs. avoid failures
- [Design for self healing](https://learn.microsoft.com/en-us/azure/architecture/guide/design-principles/self-healing)
- [Make all things redundant](https://learn.microsoft.com/en-us/azure/architecture/guide/design-principles/redundancy) 
-  [Scale-out rather than scale-up](https://learn.microsoft.com/en-us/azure/architecture/guide/design-principles/scale-out)
-  DEMO: Scale-out with Azure Container Apps
-  [Chaos engineering](https://learn.microsoft.com/en-us/azure/architecture/framework/resiliency/chaos-engineering)
- DEMO: [https://github.com/tkubica12/azure-workshops/tree/main/d-chaos-studio](https://github.com/tkubica12/azure-workshops/tree/main/d-chaos-studio)

### Microservices
- [Linux style - do one thing and do it well](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices)
- Groups defined by business function, not technology
- Contracts with others are on API level, our implementation is not your concern
- Consider service to be product
  - Make others successful using it (docs, feedback, support, lifecycle)
  - Own it from design to maintenance
  - Your language, your framework, your database, your deployment

### DevOps
- Initial idea: let Devs maintain everything and extend Agile ideas to whole lifecycle
- Reality
  - Lack of experience in security and ops lead to issues
  - Companies often just re-brand Ops to DevOps
- Good points
  - Automate yourself out of the job
  - Own business function, not specific technology
  - Break the silos, understand what others are doing

### Site Reliability Engineering
- SLOs, SLAs
- KPIs and metrics
- Error budget - get punished for over-delivering SLAs 
- PaaS vs. IaaS and composite SLA

### Platform engineering
- DevOps leads to superman that do everything - not realistic
- Shared services are essential - Platform as a Service
- [Do not compete with cloud, usually does not make sense](https://learn.microsoft.com/en-us/azure/architecture/guide/design-principles/managed-services)
- Build specific services on top that are curated for your company
- Own platform as a product
  - Make others successful using it (docs, feedback, support, lifecycle)
  - Own it from design to maintenance
  - Your cloud, your design choices, your automation, your maintenance, your security

### Safe deployment practices
- Progressive delivery (requires good metrics)
- Infra canary (Flagger, Argo Rollouts) vs. feature toggles
- A/B testing
- Green/Blue deployment
- DEMO: Argo Rollouts
- GitOps - Git as source of truth
- DEMO:  AKS GitOps with Flux

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
- DCs grouped to Availability Zones within region, <2ms apart
- Regions and control plane safe deployment processes
- Global WAN, DDoS, DNS, Auth infrastructure
- [Infrastructure map](https://infrastructuremap.microsoft.com/explore)
  
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
  - DEMO: API Management

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
  - [Asynchronous communications](https://learn.microsoft.com/en-us/azure/architecture/patterns/async-request-reply)
  - [Competing Consumers](https://learn.microsoft.com/en-us/azure/architecture/patterns/competing-consumers)
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
  - [CosmosDB consistency levekts](https://docs.microsoft.com/en-us/azure/cosmos-db/consistency-levels)
  - "Starbucks does not use 2 phase commit"
    overbooking problem and business solutions to it vs. technical ones
  - DEMO: CosmosDB global scale
- Cloud services should be you first choice
  - IaaS: 99,99% * my management and software even with 99,99% = 99,98% composite
  - PaaS: SQL DB BC = 99,995%
- [Cache-Aside](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)
- [Materialized View](https://learn.microsoft.com/en-us/azure/architecture/patterns/materialized-view)
- [CQRS](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)
- [Event sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing) vs. CRUD
  - Use change feeds to implement async fan-out (eg. CosmosDB)
  - Business events (eg. order created) may decouple logic from data implementation
- Transaction consistency
  - ACID in database
  - [Saga](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/saga/saga) pattern and compensation transactions
  - Eventual consistency with business compensation process
- [Sharding](https://learn.microsoft.com/en-us/azure/architecture/patterns/sharding)
- DEMO: Sharding in Azure Cosmos for PostgreSQL
- Shared everything vs. shared nothing vs. shared storage
- RTO and RPO

## How to choose right cloud service
- [Compute](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision)
- [Containers](https://learn.microsoft.com/en-us/azure/container-apps/compare-options)
- [Data store](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/data-store-overview)
- [Data analytics](https://learn.microsoft.com/en-us/azure/architecture/data-guide/technology-choices/analytical-data-stores)
- [AI/ML](https://learn.microsoft.com/en-us/azure/architecture/data-guide/technology-choices/data-science-and-machine-learning)
- [Messaging](https://learn.microsoft.com/en-us/azure/architecture/data-guide/technology-choices/data-science-and-machine-learning)

## Reference architectures
- [Build cloud native applications](https://learn.microsoft.com/en-us/azure/architecture/solution-ideas/articles/cloud-native-apps)
- [Microservices architecture on Azure Kubernetes Service](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/containers/aks-microservices/aks-microservices)
- [Deploy AKS and API Management with mTLS](https://learn.microsoft.com/en-us/azure/architecture/solution-ideas/articles/mutual-tls-deploy-aks-api-management)
- [Highly available zone-redundant web application](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/app-service-web-app/zone-redundant)
- [How to apply the reliable web app pattern](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/reliable-web-app/dotnet/apply-pattern)
- [Serverless web application](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/serverless/web-app)
- [Modern analytics architecture with Azure Databricks](https://learn.microsoft.com/en-us/azure/architecture/solution-ideas/articles/azure-databricks-modern-analytics-architecture)
- [Employee retention with Databricks and Kubernetes](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/ai/employee-retention-databricks-kubernetes)
- [AI enrichment with image and text processing](https://learn.microsoft.com/en-us/azure/architecture/solution-ideas/articles/cognitive-search-with-skillsets)
- [Stream processing with Azure Stream Analytics](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/data/stream-processing-stream-analytics)