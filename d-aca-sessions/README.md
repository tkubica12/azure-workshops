# Demo of Dynamic Sessions in Azure Container Apps

```bash
# Install CLI extension
az extension add --name containerapp --upgrade --allow-preview true -y

# Create a resource group
az group create --name d-aca-sessions --location eastus

# Create session pool
az containerapp sessionpool create \
    --name mypool \
    --resource-group d-aca-sessions \
    --location eastus \
    --container-type PythonLTS \
    --max-sessions 100 \
    --cooldown-period 300 \
    --network-status EgressDisabled

# Get session management API endpoint
export sapi=$(az containerapp sessionpool show \
    --name mypool \
    --resource-group d-aca-sessions \
    --query 'properties.poolManagementEndpoint' -o tsv)

# Get Entra token
export token=$(az account get-access-token --resource https://dynamicsessions.io --query accessToken -o tsv)

# Execute code in new session
export sessionId="mysession123"

curl -X POST "$sapi/code/execute?api-version=2024-02-02-preview&identifier=$sessionId" \
    -H "Authorization: Bearer $token" \
    -H "Content-Type: application/json" \
    -d '{
    "properties": {
        "codeInputType": "inline",
        "executionType": "synchronous",
        "code": "import socket\nprint(f\"Hello from {socket.gethostname()}!\")"
    }
}'

# Execute code in existing session writing some file
curl -X POST "$sapi/code/execute?api-version=2024-02-02-preview&identifier=$sessionId" \
    -H "Authorization: Bearer $token" \
    -H "Content-Type: application/json" \
    -d '{
    "properties": {
        "codeInputType": "inline",
        "executionType": "synchronous",
        "code": "with open(\"/mnt/data/hello.txt\", \"w\") as f:\n    f.write(\"Hello from session!\")"
    }
}'

# Check session files
curl "$sapi/files?api-version=2024-02-02-preview&identifier=$sessionId" \
    -H "Authorization: Bearer $token" \
    -H "Content-Type: application/json"

# Download file from session
curl "$sapi/files/content/hello.txt?api-version=2024-02-02-preview&identifier=$sessionId" \
    -H "Authorization: Bearer $token" \
    -H "Content-Type: application/json"
```