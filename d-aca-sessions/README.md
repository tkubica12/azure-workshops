# Demo of Dynamic Sessions in Azure Container Apps
## Demo in portal
You can use portal to see quick example of running code in ACA sessions.

## Demo using API from Bash
In this demo we will explore API of ACA sessions using bash and curl.

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

## Demo using API from Python using integrated framework such as LangChain
In this demo we will explore API of ACA sessions using Python and LangChain.

First create conda environment and install packages.

```bash
conda create -n aca-sessions python=3.11
conda activate aca-sessions
pip install -r requirements.txt
```

Run the code simple.py that demonstrate simple execution and see output:

```json
{
  "$id": "2",
  "status": "Success",
  "stdout": "Answer is 40\n",
  "stderr": "",
  "result": 40,
  "executionTimeInMilliseconds": 10
}
```

Run the code input_files.py that demonstrate uploading files to session and see output:

```json
{
  "$id": "2",
  "status": "Success",
  "stdout": "",
  "stderr": "",
  "result": 36.017857142857146,
  "executionTimeInMilliseconds": 27
}
```

Run the code plot.py that demonstrate plotting and file output.png.

Now let's try with Azure OpenAI to create code that will be executed in ACA session. Note you can use any model including open source orunning locally.

Export connection details - see .env.sample file

Run script in agent.py and see steps and results. LLM will understand the question, create Python code that gets executed in ACA session and return the result.

```
> Entering new AgentExecutor chain...

Invoking: `Python_REPL` with `import math
result = math.sin(math.pi)
result`


{
  "result": 1.2246467991473532e-16,
  "stdout": "",
  "stderr": ""
}
Invoking: `Python_REPL` with `import random
random_number = random.uniform(5, 10)
random_number`
responded: The sine of \(\pi\) is approximately \(1.2246467991473532 \times 10^{-16}\), which is a very small positive number.

Since it is positive, I will generate a random number between 5 and 10.

{
  "result": 6.443740307405746,
  "stdout": "",
  "stderr": ""
}

The random number generated between 5 and 10 is approximately \(6.44\).

> Finished chain.
```