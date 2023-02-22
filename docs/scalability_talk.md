Designing, deploying and managing scalable applications in cloud

How to design scalable application? Make sure components are independently scalable using microservices pattern, use asynchronous communication whenever you can. And what about data layer? Consider splitting reads and writes with patterns like CQRS, look into highly scalable NoSQL or object stores and you may even replace database-enforced ACID with saga pattern, event sourcing and compensating transactions.

- [Microservices](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices)
- [Scale-out](https://learn.microsoft.com/en-us/azure/architecture/guide/design-principles/scale-out)
- [CQRS](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)
- [Event sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
- [Competing Consumers](https://learn.microsoft.com/en-us/azure/architecture/patterns/competing-consumers)
- [Saga](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/saga/saga)
- [Cache-Aside](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)
- [async](https://learn.microsoft.com/en-us/azure/architecture/patterns/async-request-reply)
- [Materialized View](https://learn.microsoft.com/en-us/azure/architecture/patterns/materialized-view)


How to deploy scalable application? Prefer serverless capabilities in cloud or at least container platform, but note even virtual machines can scale well if done right. Avoid unique snowflake scaled-up pets, always target cattle, immutability and vertical scaling. Leverage highly scalable cloud services instead of working this out yourself such as identity, messaging, eventing, caching or data layer services. Having data analytics problem? Consider splitting data and compute layers to form lake house architectures.

Demos:
- Compute - compare scaling capabilities between compute, container and function
  - Virtual Machine Scale Set
  - Container Apps
  - Functions
- Database - showcase and compare scaling of traditional RDMS vs. distributed hyperscale SQL vs. world of NoSQL
  - Azure SQL Business Critical
  - Azure SQL hyperscale
  - Azure Cosmos DB
- Eventing
  - Event Hub Standard - 40 TUs = 1000 - 40 000 ingress messages per second
  - Event Hub Premium - 16 PUs = 10 000 - 160 000 ingress messages per second
  - Event Hub Dedicated - 10 CUs = 100 000 - 1 000 000 ingress messages per second ... and more available upon service request
- Databricks - split storage and compute, autoscale

How you manage and autoscale scalable applications? Move from infrastructure monitoring to application oriented solution using open source APIs/SDKs like OpenTelemetry together with Azure Monitor - logs and metrics are important, but tracing is starting to be key. Use application or business oriented metrics to drive scaling decisions eg. using KEDA in Kubernetes. Make sure everything is managed as a code, stored in Git, deployed using CI/CD pipelines and GitOps. Setup proper FinOps strategy.

Demos:
- Pull-based GitOps
- Application Insights