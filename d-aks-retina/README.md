# Using Retina project for network observability in AKS
In this demo I will install Retina manually and connect it with Azure Grafana and Prometheus. Later you will be able to use fully managed Retina as part of AKS platform.

## Create AKS cluster
```bash
# Create Resource Group
az group create --name d-aks-retina --location swedencentral

# Create Azure Grafana
az grafana create -n tomaskubicagrafana -g d-aks-retina

# Create Azure Monitor workpace
az resource create -n tomaskubicamonitorworkspace -g d-aks-retina --namespace microsoft.monitor --resource-type accounts --location swedencentral --properties '{}'

# Create AKS cluster
az aks create -g d-aks-retina \
    -n d-aks-retina \
    -c 2 \
    -x \
    -s Standard_B2s \
    --enable-azure-monitor-metrics \
    --enable-network-observability \
    --grafana-resource-id  $(az resource show -n tomaskubicagrafana -g d-aks-retina --resource-type "microsoft.dashboard/grafana" --query id -o tsv) \
    --azure-monitor-workspace-resource-id $(az resource show -n tomaskubicamonitorworkspace -g d-aks-retina --resource-type "Microsoft.Monitor/accounts" --query id -o tsv)

# Get AKS credentials
az aks get-credentials -g d-aks-retina -n d-aks-retina --overwrite-existing --admin
```

## Install Retina project on Linux PC
```bash
# Install Go
rm -rf /usr/local/go
wget https://go.dev/dl/go1.22.1.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.22.1.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin

# Install helm
wget https://get.helm.sh/helm-v3.14.3-linux-amd64.tar.gz
tar -zxvf helm-v3.14.3-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/sbin/helm
rm -rf linux-amd64

# Clone repository
git clone https://github.com/microsoft/retina.git

# Build remote context version
cd retina
make helm-install-advanced-remote-context
```