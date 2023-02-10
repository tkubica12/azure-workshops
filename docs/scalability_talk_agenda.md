Designing, deploying and managing scalable applications in cloud

How to design scalable application? Make sure components are independently scalable using microservices pattern, use asynchronous communication whenever you can. And what about data layer? Consider splitting reads and writes with patterns like CQRS, look into highly scalable NoSQL or object stores and you may even replace database-enforced ACID with saga pattern, event sourcing and compensating transactions.

How to deploy scalable application? Prefer serverless capabilities in cloud or at least container platform, but note even virtual machines can scale well if done right. Avoid unique snowflake scaled-up pets, always target cattle, immutability and vertical scaling. Leverage highly scalable cloud services instead of working this out yourself such as identity, messaging, eventing, caching or data layer services. Having data analytics problem? Consider splitting data and compute layers to form lake house architectures.

How you manage and autoscale scalable applications? Move from infrastructure monitoring to application oriented solution using open source APIs/SDKs like OpenTelemetry together with Azure Monitor - logs and metrics are important, but tracing is starting to be key. Use application or business oriented metrics to drive scaling decisions eg. using KEDA in Kubernetes. Make sure everything is managed as a code, stored in Git, deployed using CI/CD pipelines and GitOps. Setup proper FinOps strategy.

