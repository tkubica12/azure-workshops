# Highly available cloud native apps in cloud

## Concepts

### Tolerate vs. avoid failures
- Scale-out rather than scale-up
- Chaos engineering

### Microservices
- "Linux style" - do one thing and do it well
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
- Do not compete with cloud, does not make sense
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
- DCs grouped to Availability Zones within region, <2ms apart
- Regions and control plane safe deployment processes
- Global WAN, DDoS, DNS, Auth infrastructure
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
- Shared everything vs. shared nothing vs. shared storage
- RTO and RPO

## SaaS point of view

### Business model and its aspects
- With SaaS you ARE responsible for running and securing your app, you no longer just ship code
- Bug is bad, loosing customer data or have them stolen by hackers or causing outage is way worse
- Models:
  - Ship code, customer install and manage (provide modern way to deploy, give them container images and Helm template for example)
  - You manage, customer runs in their cloud (possible, but hard)
  - Single-tenant managed app (managed instance) - reuse what you have, provide service, easier to sell to existing customers
  - Multi-tenant SaaS - economy of scale, but needs big redesign, usually different model, harder to sell to existing customers
- You unfortunately often need to chase multiple models at once:
  - Regulated sector might demand running in their premises
  - Big significant customers might demand isolation and traditional features (eg. managing versions, costs, etc.)
  - New and small customers might prefer pure SaaS
  - Problem with history -> multi-tenant SaaS needs to be rewritten and will have a lot of feature gaps compared to legacy version

### Single-tenant managed app (managed instance)
- Close to code of traditional app
- You can reuse deployment procedures with self-managed model 
  (eg. provide your Helm templates and built containers to customers)
- Easily isolate tenants from performance ans security perspective
- More predictable pricing/margin structure
- "Enterprise-grade" features such as update when you are ready or update test instance first
- Personalized features (you can deploy different code)
- Harder to manage, support and innovate on -> higher cost in long-run
- Some economy of scale options not achievable (you leave margin on the table in long run)
- You usually create deployment environment with some self-service capabilities
- Build central monitoring solution

### Multi-tenant app
- Much harder to build, but highly efficient when done right
- Always green strategy -> not welcome by some customers, but great for your support cost and overall experience
- Harder to provide security isolation - separate encryption keys, sometimes separate storage accounts or even database instances (give one example from SK)
- Harder to provide performance guarantees -> noisy neighbor problem
- Harder to provide data residency guarantees
- More difficult cost model, focus on defining SLAs like "will be processed in less than X minutes"
- Scalability friendly architecture is a key as we discussed before:
  - Async as much as possible
  - State can become bottleneck, investigate CQRS and event sourcing, investigate saga pattern vs. ACID on DB level etc.
  - Everything automated

## Relevant cloud services

### Compute
- IaaS with Virtual Machines
- Managed Kubernetes (Azure Kubernetes Service)
- Higher-level container platforms and serverless (Azure Container Apps, Azure Functions)

### Content delivery and API management
- Static WebApps
- Azure Front Door
- Azure CDN
- Azure API Management

### Operational storage
- Blob storage
- Managed relational databases (SQL, MySQL, PostgreSQL)
- NoSQL (CosmosDB with SQL, Mongo, Cassandra or Gremlin API)
- Semi-structured analytics-optimized (Azure Data Explorer)
- Full-text oriented (Azure Cognitive Search)

### Data-analytics
- Data Lake (Azure Data Lake Storage)
- Spark-based processing (Azure Databricks)
- Data-warehouse + spark processing + ETL (Azure Synapse Analytics)
- Stream processing (Azure Stream Analytics or Azure Databricks)

### Eventing and messaging
- Event Grid (push)
- Event Hub (pull, large scale, Kafka-like)
- Service Bus (traditional queuing including exactly-once delivery)

### Observability
- Azure Managed Grafana (metrics UI)
- Azure Monitor for Prometheus (metrics backend)
- Azure Log Analytics (logs backend)
- Azure Application Insights (app logging and tracing)