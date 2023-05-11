resource "azurerm_virtual_network" "hybrid" {
  name                = "hybrid-vnet"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.55.0.0/16"]
}

resource "azurerm_subnet" "k3s" {
  name                 = "k3s-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.hybrid.name
  address_prefixes     = ["10.55.0.0/24"]
}

resource "azurerm_network_interface" "k3s" {
  name                = "k3s-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.k3s.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_linux_virtual_machine" "k3s" {
  name                            = "k3s"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  size                            = "Standard_B2s"
  admin_username                  = "tomas"
  admin_password                  = "Azure12345678"
  disable_password_authentication = false

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.hybrid.id
    ]
  }

  boot_diagnostics {}

  network_interface_ids = [
    azurerm_network_interface.k3s.id,
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  custom_data = base64encode(local.script)

  depends_on = [
    azurerm_role_assignment.hybrid,
  ]
}

resource "azurerm_user_assigned_identity" "hybrid" {
  name                = "hybrid-identity"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_resource_group" "hybrid" {
  name     = "d-aks-defender-hybrid"
  location = "westeurope"
}

resource "azurerm_role_assignment" "hybrid" {
  role_definition_name = "Contributor"
  scope                = azurerm_resource_group.hybrid.id
  principal_id         = azurerm_user_assigned_identity.hybrid.principal_id
}

data azurerm_client_config "current" {}

resource "azurerm_role_assignment" "arc_kube" {
  role_definition_name = "Azure Arc Kubernetes Viewer"
  scope                = azurerm_resource_group.hybrid.id
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_role_assignment" "arc_admin" {
  role_definition_name = "Azure Arc Enabled Kubernetes Cluster User Role"
  scope                = azurerm_resource_group.hybrid.id
  principal_id         = data.azurerm_client_config.current.object_id
}

locals {
  script = <<SCRIPT
#!/bin/sh
echo *** Installing K3s ***
curl -sfL https://get.k3s.io | sh -

echo *** Installing Helm ***
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

echo *** Installing Azure CLI ***
apt-get update
apt-get install -y ca-certificates curl apt-transport-https lsb-release gnupg
curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/microsoft.asc.gpg > /dev/null
AZ_REPO=$(lsb_release -cs)
echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" | tee /etc/apt/sources.list.d/azure-cli.list
apt-get update
apt-get install -y azure-cli

echo *** Installing CLI extensions ***
az extension add --name connectedk8s
az extension add --name k8sconfiguration
az extension add --name k8s-extension

echo *** Logging to Azure ***
az login --identity --allow-no-subscriptions

echo *** Onboard cluster ***
az connectedk8s connect --name hybrid-k8s --resource-group ${azurerm_resource_group.hybrid.name}

echo *** Onboard cluster ***
az k8s-extension create --cluster-type connectedClusters \
    --cluster-name hybrid-k8s \
    --resource-group ${azurerm_resource_group.hybrid.name} \
    --extension-type Microsoft.PolicyInsights \
    --name azurepolicy

az k8s-extension create --cluster-type connectedClusters \
    --cluster-name hybrid-k8s \
    --resource-group ${azurerm_resource_group.hybrid.name} \
    --extension-type microsoft.azuredefender.kubernetes \
    --name azuredefender \
    --configuration-settings logAnalyticsWorkspaceResourceID=${azurerm_log_analytics_workspace.hybrid.id}

kubectl create clusterrolebinding demo-user-binding --clusterrole cluster-admin --user=${data.azurerm_client_config.current.object_id}

git clone https://github.com/tkubica12/azure-workshops.git
cd azure-workshops/d-aks-defender
kubectl apply -k ./kubernetes_runtime
kubectl apply -k ./kubernetes_api
SCRIPT
}
