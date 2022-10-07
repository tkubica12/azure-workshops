# AKS with federated identity using User Managed Identity and Terraform
We will demonstrate next/gen identity solution for your containers running in AKS:
- User Managed Identity can be easily managed with Terraform requiring no direct access to AAD
- Federated identity solution (AKS OIDC with AAD federation) allows for no-credentials needed approach and replaces previous pod-identity solution
- Sidecar can be used to simulate Azure Metadata Endpoint so no change in application code is required if it uses managed identity already