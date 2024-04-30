echo ### Installing services
apt update
apt install -y nginx jq

echo ### Installing Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
