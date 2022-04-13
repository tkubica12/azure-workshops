# Kubernetes Operators talk

## 1.  How Kubernetes controllers and resources work?
- Desired state of resources -> stored on API server
- Controller -> responsible for ensuring desired state is met
- Reconcilation loop -> controller constantly checks for any changes
  in both desired and actual state and acts when they differ
- DEMO - let's play with ReplicaSet

## 2. Finding better single source of truth
- Kubernetes API server is not good storage for state
- Git is best for this and comes with operational model also (GitOps)
- Use Flux v2 (managed in AKS, great for platform) or ArgoCD (more app focused)
- Advantages using GitOps
  - Version control and release management
  - Change management (pull requests, branching policies, ...)
  - Work planning and collaboration (issues, dicussions, ...)
  - Support for any number of clusters

## 3. Keep things DRY (Don't Repeat Yourself)
- Copy and pasting something? 
  Stop and thing, you are likely doing things wrong
- Helm style -> Use template language to create abstractions
- Kustomize style -> Inherit something and patch what you need to change
- Both are different, both have important advantages, so learn both

## 4. Flux v2 operator
- Operator is using techniques we have already seen, 
  but with custom logic (controller) and custom resources (CRDs)
- Flux v2 makes sure what is in your Git is applied to your cluster
- DEMO -> see various CRDs and controllers (source, helm, kustomize)

## 5. Operators to manage specific stateful applications
- Running in Azure? Always prefer PaaS if available !
  remember that Operator != SLA
- Operators can incorporate ops procedures to help you run stateful workloads
- Examples include Azure Data Services, MongoDB, PostgreSQL, Redis, MySQL,
  Kafka, Elastic, Greenplum, RabbitMQ, ...
- DEMO -> Azure SQL operator for any Kubernetes (including GKE or OpenShift)

## 6. Operators to manage cloud resources
- Operators can manage resources outside of Kubernetes, such as in Azure
- CRDs = Azure resources
- Cloud-vendor operators can deploy vendor resources 
  (sometimes can be pluged in to Crossplane)
- Crossplane is multi-cloud and supports adding obstractions on top
- DEMO - > Azure Service Operator to deploy Azure Database for PostgreSQL

## 7. Operators to enhance Kubernetes behavior
- Operators are often perceived as single purpose solutions,
  but the same patterns can be used to enhance general capabilities
- Examples include API GWs, scalers, service meshes, progressive delivery
- DEMO -> Argo Rollouts for progressive delivery
- DEMO -> KEDA scaler that includes scale to zero (serverless behavior)

## 8. Operators to build application platforms on top of Kubernetes
- Described patterns allow to build complete application platforms on top of Kubernetes
- Examples include DAPR, KNative, Kubeless, Fission
- DEMO -> DAPR platform

