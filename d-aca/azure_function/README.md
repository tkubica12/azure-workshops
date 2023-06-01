## Azure Function
```bash
az storage account create -n tomasacafcedemo -g aca
az storage queue create -n myqueue --account-name tomasacafcedemo
export QUEUE_SAS=$(az storage account generate-sas --permissions cdlruwap \
    --account-name tomasacafcedemo \
    --services qb \
    --resource-types sco \
    --expiry "2100-01-01T01:00Z" \
    --account-key $(az storage account keys list -n tomasacafcedemo -g aca --query "[0].value" -o tsv) \
    -o tsv)

export QUEUE_CONNECTION_STRING="BlobEndpoint=https://tomasacafcedemo.blob.core.windows.net/;QueueEndpoint=https://tomasacafcedemo.queue.core.windows.net/;FileEndpoint=https://tomasacafcedemo.file.core.windows.net/;TableEndpoint=https://tomasacafcedemo.table.core.windows.net/;SharedAccessSignature=$QUEUE_SAS"

cd azure_function
python -m venv .venv
source .venv/bin/activate

#func init --worker-runtime python --docker -m V2

docker build -t ghcr.io/tkubica12/azure_function:latest .
echo $GHCR_TOKEN | docker login ghcr.io -u tkubica12 --password-stdin
docker push ghcr.io/tkubica12/azure_function:latest

# Optional local test
docker run -it --rm -e queueConnectionString=$QUEUE_CONNECTION_STRING ghcr.io/tkubica12/azure_function:latest

# Deploy function to Azure Container Apps
az extension add --name containerapp --upgrade -y
az functionapp create --name myfunction \
    --storage-account tomasacafcedemo \
    --environment aca-env \
    --resource-group aca \
    --functions-version 4 \
    --runtime python \
    --image ghcr.io/tkubica12/azure_function:latest
```