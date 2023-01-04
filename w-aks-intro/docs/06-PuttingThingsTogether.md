# Lab 6 - Putting things together to ease deployment, releases and environments using Kustomize (or Helm)
In this lab we will stop modifying YAML files directly as it does not scale, is error prone and leads to a lot of copy and paste with resulting errors and complexity.

Why we need to change this?
- Everytime we manually modify YAML we risk to break it and introduce errors.
- Everyone needs to understand everything to be able to do modifications.
- If you need different environments/instances with small changes between the two (app version, number of replicas, configs) you need to create manualy copy and keep it in sync. Copy and paste always leads to errors over time including test environment becoming irrelevant (because you test something else than is rolled into production due to inconsistencies by copies over time).

Two major (and very different approaches):
- **Helm** is still most used tool, but Kustomize has taken a lot of share from it.
  - Helm is using templating language (Go templates) so you create your own abstractions/interfaces and language is very powerful (including loops etc.). Therefore Helm is much more flexible and can create very simple interface for users abstracting complexity away. It is harder to create, but easier to consume.
  - Helm is taking care of whole lifecycle (eg. supports rollback operation), but with todays maturity of CI/CD systems this is not as relevant as before.
  - Your abstractions can also be disadvantage - you can easily introduce inconsistencies between projects (eg. parameter imageTag in one project and image.tag in other one) so maintaining good quality of your abstractions creates additional overhead.
  - If you need to change something, that has not been parametrized as input, you are in trouble. This might lead to "everything is parameter" over time making things much more complex.
- **Kustomize** is taking simpler approach  and rather than templating is using patching. 
  - You are not defining your own abstractions, but you create patch layers over basic YAML files. You can change any Kubernetes parameter without need to template it or create abstraction for it. 
  - On the other hand when using Kubernetes you need more knowledge about Kubernetes so for first time users it is easier to author, but little more difficult to consume.
  - Kustomize is built into kubectl so you do not need to install anything.
  - Kustomize has become popular with pull-based GitOps deployment styles.

In our lab we will use Kustomize.

In your resources/kustomize folder there is base folder containing YAML files and environments folder currently with one subfolder (test). 

Make sure prefix is still configured in your terminal (bash):

```bash
export prefix="tomaskubica8"
```

If you use powershell:

```powershell
$prefix="tomaskubica8"
```

We will now deploy test environment of this application. First let's create new namespace in Kubernetes and create secret with PostgreSQL connection string there.

```bash
# Create namespace
kubectl create namespace test 

# Create Secret in Bash in namespace test
kubectl create secret generic psql-secret --namespace test --from-literal=postgresqlurl='jdbc:postgresql://'${prefix}'-psql.postgres.database.azure.com:5432/todo?user=psqladmin&password=Azure12345678!&ssl=true'

# Create Secret in PowerShell in namespace test
kubectl create secret generic psql-secret --namespace test --from-literal=postgresqlurl="jdbc:postgresql://${prefix}-psql.postgres.database.azure.com:5432/todo?user=psqladmin&password=Azure12345678!&ssl=true"
```

Look at base folder - you will se YAML files that are familiar to you. Only difference is they do not contain changes you introduced during previous labs. kustomization.yaml file lists links to those files (please note - there are some addition YAML files in base not yet referenced - keep it as it is now, we will use those in following labs). We will work in environments/test folder that will contain customizations for your test environment:
- open kustomization.yaml file and note:
  - We are referencing our base as starting point
  - We target this deployment to namespace test
  - In images section change netName to reflect your container registry
  - patchesStrategicMerge refers to web-deployment.yaml file that contains basic identification of object and field we want to change (replicas in our case -> to be 2)
  - For ingress we are using different patch strategy - direct patch of field rather then merge - change value to fit your FQDN. Because we now have both test and production version running on the same IP, we will recognize apps with hostname. This requires DNS and for simplicity we will use nip.io. So your test will run on test.yourip.nip.io while your production on prod.yourip.nip.io.

So - do not touch base folder at all, but modify files under environments/test and let's deploy this.

```bash
cd ../kustomize
kubectl apply -k environments/test
kubectl get pods -n test
```

Open browser and you should see application in test environment running fine using v2.

Now it is your turn - create **production environment** with following requirements:
- web will use v1 (v2 is not ready for production)
- both web and api should run in 3 replicas
- production must run in production namespace
- external URL should be prod.yourip.nip.io
- we will use the same database for simplicity (sure in real life test environment will have different DB = different connection string in secret)

Prepare production folder in your environments, create kustomization files there, production configuration, deploy and make sure application is working fine.

Tips:
- Have you created namespace?
- Have you created secret in new namespace?
- Have you added patches files and references in kustomization.yaml to get 3 replicas of api and web?
- Have you changed host for ingress?

# Optional challenge - create application template using Helm
Rework solution using Helm template instead of Kustomize. Make sure template has configurable parameters such as:
- image name/tag/registry
- number of replicas
- ingress host

Make sure you have just one template, but 2 values file to deploy to test vs. production.