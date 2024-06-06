# Application Gateway in private network with certificate from Key Vault
First deploy environment with jump server. Then use SSH to connect to it and continue from there.

```bash
# Connect to jump server
az serial-console connect -n jump -g rg-appgw-kv-cert

# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure using managed identity
az login --identity

# Install Terraform
sudo apt-get install -y gnupg software-properties-common
wget -O- https://apt.releases.hashicorp.com/gpg | \
gpg --dearmor | \
sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update
sudo apt-get install terraform

# Download code
git clone https://github.com/tkubica12/azure-workshops.git
cd azure-workshops
cd d-appgw-kv

# Deploy appgw
cd appgw
terraform init
terraform apply -auto-approve
```