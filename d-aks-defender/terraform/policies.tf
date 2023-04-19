// Kubernetes cluster should not allow privileged containers
resource "azurerm_resource_policy_assignment" "no_priv_containers" {
  name                 = "no_priv_containers"
  resource_id          = azurerm_kubernetes_cluster.main.id
  policy_definition_id = "/providers/Microsoft.Authorization/policyDefinitions/95edb821-ddaf-4404-9732-666045e056b4"

  parameters = <<EOF
{
    "effect": {"value": "Deny"},
    "namespaces": {"value": ["policy-demo"]}
}
EOF
}

// Kubernetes clusters should be accessible only over HTTPS
resource "azurerm_resource_policy_assignment" "https_ingress_only" {
  name                 = "https_ingress_only"
  resource_id          = azurerm_kubernetes_cluster.main.id
  policy_definition_id = "/providers/Microsoft.Authorization/policyDefinitions/1a5b4dca-0b6f-4cf5-907c-56316bc1bf3d"

  parameters = <<EOF
{
    "effect": {"value": "Deny"},
    "namespaces": {"value": ["policy-demo"]}
}
EOF
}

// Kubernetes cluster pods should only use allowed volume types
// Use modern drivers only (CSI), do not allow hostPath (security risk) and emptyDir (use PVC to maintain isolation)
resource "azurerm_resource_policy_assignment" "limit_volumes" {
  name                 = "limit_volumes"
  resource_id          = azurerm_kubernetes_cluster.main.id
  policy_definition_id = "/providers/Microsoft.Authorization/policyDefinitions/16697877-1118-4fb1-9b65-9898ec2509ec"

  parameters = <<EOF
{
    "effect": {"value": "Deny"},
    "allowedVolumeTypes": {"value": ["projected", "csi", "secret", "configMap", "persistentVolumeClaim"]},
    "namespaces": {"value": ["policy-demo"]}
}
EOF
}

// Kubernetes clusters should not allow container privilege escalation
resource "azurerm_resource_policy_assignment" "no_priv_escalation" {
  name                 = "no_priv_escalation"
  resource_id          = azurerm_kubernetes_cluster.main.id
  policy_definition_id = "/providers/Microsoft.Authorization/policyDefinitions/1c6e92c9-99f0-4e55-9cf2-0c234dc48f99"

  parameters = <<EOF
{
    "effect": {"value": "Deny"},
    "namespaces": {"value": ["policy-demo"]}
}
EOF
}

// Kubernetes cluster containers should not use forbidden sysctl interfaces
resource "azurerm_resource_policy_assignment" "no_sysctl" {
  name                 = "no_sysctl"
  resource_id          = azurerm_kubernetes_cluster.main.id
  policy_definition_id = "/providers/Microsoft.Authorization/policyDefinitions/56d0a13f-712f-466b-8416-56fb354fb823"

  parameters = <<EOF
{
    "effect": {"value": "Deny"},
    "forbiddenSysctls": {"value": ["*"]},
    "namespaces": {"value": ["policy-demo"]}
}
EOF
}


// Kubernetes clusters should not grant CAP_SYS_ADMIN security capabilities
resource "azurerm_resource_policy_assignment" "no_sysadmin_cap" {
  name                 = "no_sysadmin_cap"
  resource_id          = azurerm_kubernetes_cluster.main.id
  policy_definition_id = "/providers/Microsoft.Authorization/policyDefinitions/d2e7ea85-6b44-4317-a0be-1b951587f626"

  parameters = <<EOF
{
    "effect": {"value": "Deny"},
    "namespaces": {"value": ["policy-demo"]}
}
EOF
}

// Kubernetes clusters should use internal load balancers
resource "azurerm_resource_policy_assignment" "no_external_lb" {
  name                 = "no_external_lb"
  resource_id          = azurerm_kubernetes_cluster.main.id
  policy_definition_id = "/providers/Microsoft.Authorization/policyDefinitions/3fc4dc25-5baf-40d8-9b05-7fe74c1bc64e"

  parameters = <<EOF
{
    "effect": {"value": "Deny"},
    "namespaces": {"value": ["policy-demo"]}
}
EOF
}

// Kubernetes clusters should disable automounting API credentials
resource "azurerm_resource_policy_assignment" "no_api_credentials" {
  name                 = "no_api_credentials"
  resource_id          = azurerm_kubernetes_cluster.main.id
  policy_definition_id = "/providers/Microsoft.Authorization/policyDefinitions/423dd1ba-798e-40e4-9c4d-b6902674b423"

  parameters = <<EOF
{
    "effect": {"value": "Deny"},
    "namespaces": {"value": ["policy-demo"]}
}
EOF
}

