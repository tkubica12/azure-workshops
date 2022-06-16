# Demo - AKS developer experience with Draft v2, GitHub and Web Application Routing (managed Ingress)
In this demo we will look into dev experience for AKS that is being worked on and is as time of this writing available in preview. Main purpose is to go from source code to running securely accessed application in single command basically bringing some of PaaS experiences to world of Kubernetes. Under covers this includes Draft, GitHub Actions, AKS, managed NGINX Ingress, Open Service Mesh with E2E encryption, Key Vault for certificate storage and External DNS with Azure DNS to provide public name resolution.

## Prepare AKS, DNS, certificate and other componens

```bash
# Install the aks-preview extension
az extension add --name aks-preview

# Update the extension to make sure you have the latest version installed
az extension update --name aks-preview

# Create public DNS zone
az network dns zone create -g akswebrouting -n myapp.demo

# Create AKS with Web Application Routing, Open Service Mesh and KV secrets provider
az group create -n akswebrouting -l westeurope
az aks create -n akswebrouting \
  -g akswebrouting \
  -c 1 \
  -x \
  -k 1.23.5 \
  --network-plugin azure \
  -s Standard_B4ms \
  --enable-addons web_application_routing,open-service-mesh,azure-keyvault-secrets-provider \
  --dns-zone-resource-id $(az network dns zone show -g akswebrouting -n myapp.demo --query id -o tsv)

az aks get-credentials --admin --overwrite-existing -n akswebrouting -g akswebrouting
kubectl create namespace myweb
osm namespace add myweb

# Create Key Vault and give webapprouting identity access rights to read secrets and certificates
az keyvault create -n mywebvault -g akswebrouting --enable-rbac-authorization
export AKSRG=$(az aks show -n akswebrouting -g akswebrouting --query nodeResourceGroup -o tsv)
export webroutingid=$(az identity show -n webapprouting-akswebrouting -g $AKSRG --query principalId -o tsv)
export kvId=$(az keyvault show -n mywebvault -g akswebrouting --query id -o tsv)
az role assignment create --scope $kvId --role "Key Vault Administrator" --assignee  $(az account show --query user.name -o tsv)
az role assignment create --scope $kvId --role Reader --assignee-object-id  $webroutingid
az role assignment create --scope $kvId --role "Key Vault Certificates Officer" --assignee-object-id  $webroutingid
az role assignment create --scope $kvId --role "Key Vault Secrets User" --assignee-object-id  $webroutingid

# Give webapprouting identity access rights 
export AKSRG=$(az aks show -n akswebrouting -g akswebrouting --query nodeResourceGroup -o tsv)
export webroutingid=$(az identity show -n webapprouting-akswebrouting -g $AKSRG --query principalId -o tsv)
az role assignment create --scope $(az network dns zone show -g akswebrouting -n myapp.demo --query id -o tsv) \
  --role "DNS Zone Contributor" \
  --assignee-object-id  $webroutingid



# Generate self-signed certificate for demo purposes
az keyvault certificate create --vault-name mywebvault -n myappdemocert -p '{
  "issuerParameters": {
    "certificateTransparency": null,
    "name": "Self"
  },
  "keyProperties": {
    "curve": null,
    "exportable": true,
    "keySize": 2048,
    "keyType": "RSA",
    "reuseKey": true
  },
  "lifetimeActions": [
    {
      "action": {
        "actionType": "AutoRenew"
      },
      "trigger": {
        "daysBeforeExpiry": 90,
        "lifetimePercentage": null
      }
    }
  ],
  "secretProperties": {
    "contentType": "application/x-pkcs12"
  },
  "x509CertificateProperties": {
    "ekus": [
      "1.3.6.1.5.5.7.3.1"
    ],
    "keyUsage": [
      "cRLSign",
      "dataEncipherment",
      "digitalSignature",
      "keyEncipherment",
      "keyAgreement",
      "keyCertSign"
    ],
    "subject": "C=US, ST=WA, L=Redmond, O=Contoso, OU=Contoso HR, CN=www.myapp.demo",
    "subjectAlternativeNames": {
      "dnsNames": [
        "*.myapp.demo"
      ],
      "emails": [
        "hello@myapp.demo"
      ],
      "upns": []
    },
    "validityInMonths": 24
  }
}'

```

## From code to running application



```bash
# Initialize Draft
az aks draft create

  [Draft] --- Detecting Language ---
  ✔ yes
  [Draft] --> Draft detected Go (100.000000%)

  [Draft] --- Dockerfile Creation ---
  Please Enter the port exposed in the application: 3000
  [Draft] --> Creating Dockerfile...

  [Draft] --- Deployment File Creation ---
  ✔ kustomize
  ✔ Please Enter the port exposed in the application: 3000█
  Please Enter the name of the application: web
  [Draft] --> Creating kustomize Kubernetes resources...

  [Draft] Draft has successfully created deployment resources for your project 😃
  [Draft] Use 'draft setup-gh' to set up Github OIDC.

# Create application registration for GitHub and note its appId
export appId=$(az ad sp create-for-rbac -n https://tomaskubicadraft --query appId -o tsv)

# Install GitHub CLI
[https://cli.github.com/manual/installation](https://cli.github.com/manual/installation)

# Setup GitHub
az aks draft setup-gh --app $appId --gh-repo tkubica12/azure-workshops --resource-group akswebrouting --subscription-id $(az account show --query id -o tsv) --debug
az aks draft setup-gh --app "tomaskubicadraftsp" --gh-repo tkubica12/azure-workshops --resource-group akswebrouting --subscription-id $(az account show --query id -o tsv) --provider azure --debug

# Give this account access to Azure
az role assignment create -g akswebrouting --role "Contributor" --assignee $(az ad sp list --display-name tomaskubicadraftsp --query [0].appId -o tsv)

# Create Azure Container Registry
az acr create -n tomasdraftacr15 -g akswebrouting --sku Basic --admin-enabled

# Setup workflow
az aks draft generate-workflow --cluster-name akswebrouting \
  --destination ./d-aks-devexperience \
  --container-name draftdemo \
  --resource-group akswebrouting \
  --registry-name tomasdraftacr15 \
  --branch main

# Deploy application with managed ingress
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aks-helloworld  
  namespace: myweb
spec:
  replicas: 1
  selector:
    matchLabels:
      app: aks-helloworld
  template:
    metadata:
      labels:
        app: aks-helloworld
    spec:
      containers:
      - name: aks-helloworld
        image: mcr.microsoft.com/azuredocs/aks-helloworld:v1
        ports:
        - containerPort: 80
        env:
        - name: TITLE
          value: "It works!"
---
apiVersion: v1
kind: Service
metadata:
  name: aks-helloworld
  namespace: myweb
  annotations:
    kubernetes.azure.com/ingress-host: www.myapp.demo
    kubernetes.azure.com/tls-cert-keyvault-uri: $(az keyvault certificate show --vault-name mywebvault -n myappdemocert --query id -o tsv)
spec:
  type: ClusterIP
  ports:
  - port: 80
  selector:
    app: aks-helloworld
EOF


# Cleanup
az ad sp delete --id $(az ad sp list --display-name tomaskubicadraft --query [0].appId -o tsv)
az ad app delete --id $(az ad app list --display-name https://tomaskubicadraft --query [0].appId -o tsv)
az keyvault delete -n mywebvault -g akswebrouting 
az keyvault purge -n mywebvault -l westeurope
az group delete -n akswebrouting -y

