# API Management in enterprise network using self-hosted agent in AKS
Purpose of this demo is to showcase one of API Management deployment model that supports fully private dataplane (endpoint consumers are using) together with platform-based control plane and developer portal. This setup is good choice for enterprise network because:
- Dataplane component uses call-home style - limited set of outbound FQDNs on port 443
- No need to open any inbound port
- No need to modify existing UDRs or create exceptions

More details at [https://docs.microsoft.com/en-us/azure/api-management/self-hosted-gateway-overview#connectivity-to-azure](https://docs.microsoft.com/en-us/azure/api-management/self-hosted-gateway-overview#connectivity-to-azure)

# Demo deployment
Solution is built using Terraform.

```bash
cd d-apim-in-aks/terraform
terraform init
terraform apply
```

In next step key access keys and Deploy API gateway to AKS.

```bash
# Get AKS credentials
az aks get-credentials -n apim-demo-aks -g apim-demo-aks --admin --overwrite-existing

# Get APIM gateway token
export token=$(az rest -m post -u $(terraform output -raw gateway_id)/generateToken?api-version=2021-08-01 \
    -b '{
        "keyType": "primary",
        "expiry": "'$(date -Iseconds --date="28 day")'"
        }' \
     --query value -o tsv)

# Store token as secret
kubectl create secret generic demogw-token --from-literal=value="GatewayKey $token" --type=Opaque

# Deploy
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: demogw-env
data:
  config.service.endpoint: "$(terraform output -raw apim_name).configuration.azure-api.net"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demogw
spec:
  replicas: 2
  selector:
    matchLabels:
      app: demogw
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 25%
  template:
    metadata:
      labels:
        app: demogw
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - name: demogw
        image: mcr.microsoft.com/azure-api-management/gateway:v2
        ports:
        - name: http
          containerPort: 8080
        - name: https
          containerPort: 8081
        readinessProbe:
          httpGet:
            path: /status-0123456789abcdef
            port: http
            scheme: HTTP
          initialDelaySeconds: 0
          periodSeconds: 5
          failureThreshold: 3
          successThreshold: 1
        env:
        - name: config.service.auth
          valueFrom:
            secretKeyRef:
              name: demogw-token
              key: value
        envFrom:
        - configMapRef:
            name: demogw-env
---
apiVersion: v1
kind: Service
metadata:
  name: demogw
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"
spec:
  type: LoadBalancer
  loadBalancerIP: 10.0.0.250
  externalTrafficPolicy: Local
  ports:
  - name: http
    port: 80
    targetPort: 8080
  - name: https
    port: 443
    targetPort: 8081
  selector:
    app: demogw
EOF
```

# Demo walkthrough
API Management is deployed with one mocked API, no VNET integration, but self-hosted gateway running inside AKS. Demonstrate this in portal.

From jump server demonstrate you can access mocked API internally.

```bash
# Use serial console to connect to jump server and from it connect to API
az serial-console connect -g apim-demo-aks -n jumpvm
curl http://10.0.0.250/demo/demo/items
```

