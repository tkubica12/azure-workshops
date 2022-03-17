# Introduction to Azure Kubernetes Service

Make sure you finish [preparation steps](./docs/00-PreparationAndTooling.md) before starting this workshop.

# Lab 1 - Create container registry and build our web and api applications
In this lab you will look at provided application and build it.

[guide](./docs/01-BuildApp.md)

# Lab 2 - Understand operational patterns using higher level platform Azure Container Apps
In this lab you will first use higher level platform so you can understand concepts of containers, deployments, replicas, canary releases or upgrades before you get overwhelmed by low level details of Kubernetes.

[guide](./docs/02-UnderstandOperationalPatterns.md)

# Lab 3 - Deploy Azure Kubernetes Service and first application
In this lab we will create AKS and deploy our web application.

[guide](./docs/03-DeployAksAndFirstApp.md)

# Lab 4 - Understand Deployment and services
In this lab we are going to run multiple redundant instances, investigate labels and services, load-balancincg and do rolling upgrade of our deployment.

[guide](./docs/04-UnderstandDeploymentsAndServices.md)

# Lab 5 - Complete our application by adding api, database and ingress
In this lab we will create managed database in Azure, deploy api component in Kubernetes and configure credentials to access database. Then we will expose both components via ingress so we get fully working TODO application.

[guide](./docs/05-CompleteApplication.md)

# Lab 6 - Putting things together to ease deployment, releases and environments using Kustomize (or Helm)
In this lab we will stop modifying YAML files directly as it does not scale, is error prone and leads to a lot of copy and paste with resulting errors and complexity.

[guide](./docs/06-PuttingThingsTogether.md)

# Lab 7 - Using shared persistent storage for static content
In this lab we will fix one problem with our web - its logo is part of container image. We are lucky it is very small, but what if we need to access video files from multiple replicas?

[guide](./docs/07-PerstistentStorage.md)

# Lab 8 - Using ConfigMaps to manage configuration files in containers
In this lab we will use ConfigMap to create configuration data to be injected into containers so we can change comples application configuration without rebuilding container image.

[guide](./docs/08-ApplicationConfigurations.md)

