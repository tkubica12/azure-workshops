# Principles
- Best place to store secrets is in vault (eg. Azure Key Vault)
- Application need to access vault and for that it need mechanism and identity
  - Mechanism
    - Directly from app using SDK - build into your code
    - Using helper such as sidecar - look at DAPR for universal multi-cloud approach
    - Leveraging platform feature and access via file or env - eg. Kubernetes Secrets Provider Class
  - Identity
    - Platform based identity eg. VM User Managed Identity
    - Workload based identity - different for each workload
      - App registration (Service Principal) for app (issue - how to deliver credentials in secure way)
      - Managed Identity with app per VM
      - Using Pod Identity (scalability limits, but still fully supported until replacement is GA)
      - Workload identity federation (SP-based currenty, roadmap for Managed Identity)
# Solutions
## Kubernetes Secrets
- Secrets are encrypted at rest on platform level (Microsoft-managed)
- Easy to use
- Works in every environment
- No support for customer-provided key
- No support for true multitenancy (different vaults for different apps)
- Secrets not stored in certified hardware-based vault
## Kubernetes Secrets encrypted with KMS
- Secrets are encrypted at rest using customer-provided key (stored in vault)
- Easy to use
- Works in every environment
- No support for true multitenancy (different vaults for different apps)
- Secrets not stored in certified hardware-based vault (but encryption key is)
## Secrets Provider Class
- Secrets are stored in proper vault
- Provider-specific driver, but using standard implementation (Azure, GCP, AWS and Hashicorp Vault)
- Can work in other environments
- Supports true multi-tenancy
- Hardware-based vault support
- Identity used to access vault in case of AKS:
  - Single identity (systems assigned, user-managed)
  - Per-pod identity with Pod identity (GA, fully supported)
  - Workload identity (next-gen solution, in preview as of July 2022)
## DAPR
- Platform for distributed applications
- Can run on any Kubernetes or even on VMs and IoT devices without containers
- Provides API to access secrets 
  -> allows the same application code to access different backends without change
- Identity used to access vault in case of AKS:
  - Single identity (systems assigned, user-managed)
  - Per-pod identity with Pod identity (GA, fully supported)
  - Workload identity via MSI layer
## Application
- Use SDK to different providers
- Use workload identity federation to echange Kubernetes token for AAD token
- Use Pod Identity with Managed Identity