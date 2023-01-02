# Understand Deployment and Services
In this lab we are going to run multiple redundant instances, investigate labels and services, load-balancincg and do rolling upgrade of our deployment.

We want to run our web using more replicas to balance load and provide redundancy. Modify web-deployment.yaml to increase number of replicas to 3.

Check Pods are running and also see how they spread AKS nodes (by using wide output).

```bash
kubectl get pods -o wide
```

Next we need to have representation of all those instances as single service - single DNS record with virtual IP that provides load balancing to live instances.

```bash
kubectl apply -f web-service.yaml
```

At this point service is only internal to Kubernetes cluster (we will solve access from outside in later lab). In order to test this we will deploy separate Pod for testing.

```bash
kubectl apply -f testclient-pod.yaml
```

When troubleshooting it is often helpful to exec directly into Pod to test things out. Let's do it and try to access out web service. Note you are getting responses from all 3 of its instances - load balancing works.

```bash
kubectl exec -ti testclient -- bash   # This opens session with your container
curl http://web/info
curl http://web/info
curl http://web/info
exit
```

In Kubernetes it is important to understand concept of labels which are used to identify objects. You have seen that Service was using labels as selector - all Pods that match set of such labels are part of it, traffic being balanced to those. Also Deployment (in fact ReplicaSet which it creates) is using labels to identify Pods that are part of it and reconciliation loop keeps track of desired vs. actual Pods with such labels running. We will not test this behavior.

We will use live edit (never use it in production, this is for troubleshooting only) of one of your web Pods and change label from app: web to app: somethingelse.

```bash
kubectl edit pod web-bd6c684fc-v6xfp
```

What happened? You should now see 4 web Pods running. Think about why - following commands should help you.

```bash
kubectl get pods --show-labels  # Show Pods with all labels
kubectl get pods -L app         # Show column with values of certain label
kubectl get pods -l app=web     # Show Pods where label app=web
```

As you see you modified Pod is no longer considered part of Deployment/ReplicaSet nor Service (no traffic). Modify it again and put back label app: web. What you expect to happen?

```bash
kubectl edit pod web-bd6c684fc-v6xfp
kubectl get pods --show-labels  # One of Pods got killed - desired state is 3, actual was 4
```

Let's now upgrade our application to v2 using simple rolling upgrade. First we need to understand that Deployment represents state of our application and it creates ReplicaSet which is responsible for keeping our 3 Pods running.

```bash
kubectl get deployment,replicaset
```

In order to test things out open different session, access our testclient Pod and keep curl running.

```bash
kubectl exec -ti testclient -- bash -c "while true; do curl http://web/info; sleep 0.5; done"
```

Modify web-deployment.yaml to use v2 image and deploy it. Note new ReplicaSet will be created with 1 Pod with new version. If this one works fine, it will scale v1 ReplicaSet to 2 and scale ap v2 ReplicaSet to 2. If everything goes well we will end up with v1 ReplicaSet scaled to 0 and v2 ReplicaSet scaled to 3.

```bash
kubectl get deployment,replicaset
```

Note we might loose just one or two requests - and this can get better once we properly use probes and ingress (in later lab).

# Optional challenge - scale out your application
Your AKS cluster is configured with autoscaling to add additional nodes should capacity of cluster get exceeded. Play with requests limits and replicas in your deployment so you achieve state where no additional pods can fit existing 2-node cluster and additional node gets provisioned automatically.