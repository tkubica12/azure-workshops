# AKS with federated identity using User Managed Identity, Terraform and Key Vault
We will demonstrate next/gen identity solution for your containers running in AKS:
- User Managed Identity can be easily managed with Terraform requiring no direct access to AAD
- Federated identity solution (AKS OIDC with AAD federation) allows for no-credentials needed approach and replaces previous pod-identity solution
- Sidecar can be used to simulate Azure Metadata Endpoint so no change in application code is required if it uses managed identity already
- Secrets Provides Class can be used to access secrets from Azure Key Vault via workload identity (each class is mapped to its own workload idenity so multiple different security boundaries can be used in single cluster)

## Deploy and get credentials

```bash
# Deploy infrastructure and app
cd terraform
terraform init
terraform apply

# Get cluster credentials
az aks get-credentials -n d-aks-federated-identity -g d-aks-federated-identity --admin
```

## Demonstrate workload idenity manualy and via metadata endpoint

```bash
# Check app is running
kubectl get pods

# Note your blob URL
terraform output blob_url

# Jump to container
kubectl exec -it client-identity -- /bin/bash

# AKS made token issued by OIDC available so you can exchange it for AAD token yourself
env | grep AZURE

: '
AZURE_TENANT_ID=d6af5f85-2a50-4370-b4b5-9b9a55bcb0dc
AZURE_FEDERATED_TOKEN_FILE=/var/run/secrets/azure/tokens/azure-identity-token
AZURE_AUTHORITY_HOST=https://login.microsoftonline.com/
AZURE_CLIENT_ID=4b9a2ebe-21b3-45c8-b496-645579fb4a6d
'

cat $AZURE_FEDERATED_TOKEN_FILE

: '
eyJhbGciOiJSUzI1NiIsImtpZCI6ImdXeDdWZ3dMWXdxTHZaVDdKVzlRV1l3TGU1R1U2ZEhjZEdXZ2didi05Z00ifQ.eyJhdWQiOlsiYXBpOi8vQXp1cmVBRFRva2VuRXhjaGFuZ2UiXSwiZXhwIjoxNjY1MTE5MjY2LCJpYXQiOjE2NjUxMTU2NjYsImlzcyI6Imh0dHBzOi8vd2VzdGV1cm9wZS5vaWMucHJvZC1ha3MuYXp1cmUuY29tL2Q2YWY1Zjg1LTJhNTAtNDM3MC1iNGI1LTliOWE1NWJjYjBkYy84MzMwMDcwOC1iZTFlLTQ5OTAtODdmOC1hOWY2MWM5YzIzZGUvIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJkZWZhdWx0IiwicG9kIjp7Im5hbWUiOiJjbGllbnQiLCJ1aWQiOiJmYzhmMDY2Ni1mNWI0LTQyODgtOThmNC1hZWNhOTA3OTNlYmEifSwic2VydmljZWFjY291bnQiOnsibmFtZSI6ImlkZW50aXR5MSIsInVpZCI6Ijk2MDc3ZWQwLTRhYjctNDNhNi05Njk0LTE1NjU4M2EzMTg4YiJ9fSwibmJmIjoxNjY1MTE1NjY2LCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6ZGVmYXVsdDppZGVudGl0eTEifQ.TQ6E-WOxbUjVjrEcLOscUC20wL6JB5SIi8bG-SRQDEw0JeAqGaKeMTV0fS9d7EgOLDVGQbqp9R-FytxrB024k8qGPHZ3gMN2OQSZJh0Cvh0lcMPBLCsWj75GJhNxX747ZGBe2KDQCIjbe9HXWDjZNTXfogpcO5odpN1tEFrLWjetuLWruSQe-FlCmU7qgGV19xvgTlCO1oW5VnMSr_IjV07CZz_qblo5cqsJy5yaeT0QnSoPLBcTQ-tbCdCOyc44OlZLBGc6lnDZtQEc--jtOWglcO4OtSxQf2Vr69tin1J9UyfOBk1PJ_AhLBlhpHOACy6JDtdaPFRoyozEkZOiflloH1ZmJc3Rf3DaBzhRfhvsjem0WnDRmV5-RDZDWitF0GloS9PUgBluCYi0NiniKuEkfpE-Be1dqPWHmnUnrL6iR9nEt8FOR6Ns0MgNR_e9uJvc7xLWnqyZNNSSWtzsOphyf8_mwh-1_8qx6IrbNzapvSALTiUloKnui9HuabRtdoqQ8W-VvCXC9jyQ-mlO_MZWQ5kwiyCR0ubnM8eAEf8CVwdYbpGzJqMXg_S7oU16kOM-01c1GxpiTfNH1m2Tm0nDS6tb2pDpNpVYs-c5zTCGimlggL8IssmSaqvvazG7e8j6JDkU_Jf5yPB5i3S6NLYe81REsxzDRhp7b39qHYM
'

# This is how token looks decoded

: '
{
  "aud": [
    "api://AzureADTokenExchange"
  ],
  "exp": 1665119266,
  "iat": 1665115666,
  "iss": "https://westeurope.oic.prod-aks.azure.com/d6af5f85-2a50-4370-b4b5-9b9a55bcb0dc/83300708-be1e-4990-87f8-a9f61c9c23de/",
  "kubernetes.io": {
    "namespace": "default",
    "pod": {
      "name": "client",
      "uid": "fc8f0666-f5b4-4288-98f4-aeca90793eba"
    },
    "serviceaccount": {
      "name": "identity1",
      "uid": "96077ed0-4ab7-43a6-9694-156583a3188b"
    }
  },
  "nbf": 1665115666,
  "sub": "system:serviceaccount:default:identity1"
}
'
# Exchange token yourself
apt update
apt install jq -y

scope="https://storage.azure.com/.default"
output=$(curl -X POST \
    "https://login.microsoftonline.com/$AZURE_TENANT_ID/oauth2/v2.0/token" \
    -d "scope=$scope&client_id=$AZURE_CLIENT_ID&client_assertion=$(cat $AZURE_FEDERATED_TOKEN_FILE)&grant_type=client_credentials&client_assertion_type=urn%3Aietf%3Aparams%3Aoauth%3Aclient-assertion-type%3Ajwt-bearer")

token=$(echo $output | jq -r .access_token)

# Use token to access file on storage
export BLOB_URL="https://wjqnugbhtdxymeaf.blob.core.windows.net/container/file.txt"
curl -H "Authorization: Bearer $token" \
     -H "x-ms-version: 2020-04-08" \
    $BLOB_URL

: '
My super data file
'

# Get token using metadata endpoint (very widely supported in various SDKs)
export STORAGE_ACCOUNT_URL="https://ubjbgkwmlmqrkiyf.blob.core.windows.net"
token2=$(curl -s -H Metadata:true "http://169.254.169.254/metadata/identity/oauth2/token?resource=$STORAGE_ACCOUNT_URL&client_id=$AZURE_CLIENT_ID" | jq -r '.access_token')

# Use token to access file on storage
export BLOB_URL="https://ubjbgkwmlmqrkiyf.blob.core.windows.net/container/file.txt"
curl -H "Authorization: Bearer $token2" \
     -H "x-ms-version: 2020-04-08" \
    $BLOB_URL

: '
My super data file
'
```

Note this is what application SDK might do automatically for you, eg. SQL SDK.

## Secrets provider from Key Vault using workload identity
```bash
# Jump to container
kubectl exec -it client-secrets -- /bin/bash

# Show how secret from Key Vault is mapped to file system
ls /mnt/mysecretpath/ 

: '
mysecretpath
'

cat /mnt/mysecretpath/mysecret

: '
ThisIsVerySecret!
'

# Show how secret is in env due to secret sync
echo $MY_SECRET

: '
ThisIsVerySecret!
'
```
