import os
import dotenv
import asyncio
from azure.servicebus.aio import ServiceBusClient
from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient
from azure.cosmos.aio import CosmosClient
from concurrent.futures import ThreadPoolExecutor
import json
import requests
import base64
from openai import AsyncAzureOpenAI

# Load environment variables
def get_env_var(var_name):
    value = os.environ.get(var_name)
    if not value:
        raise EnvironmentError(f"{var_name} environment variable is not set")
    return value

dotenv.load_dotenv()

azure_openai_api_key = get_env_var("AZURE_OPENAI_API_KEY")
azure_openai_endpoint = get_env_var("AZURE_OPENAI_ENDPOINT")
azure_openai_api_version = "2024-10-21"
azure_openai_deployment_name = get_env_var("AZURE_OPENAI_DEPLOYMENT_NAME")
servicebus_fqdn = get_env_var("SERVICEBUS_FQDN")
servicebus_queue = get_env_var("SERVICEBUS_QUEUE")
storage_account_url = get_env_var("STORAGE_ACCOUNT_URL")
storage_container = get_env_var("STORAGE_CONTAINER")
batch_size = int(get_env_var("BATCH_SIZE"))
max_wait_time = float(get_env_var("BATCH_MAX_WAIT_TIME"))
cosmos_account_url = get_env_var("COSMOS_ACCOUNT_URL")
cosmos_db_name = get_env_var("COSMOS_DB_NAME")
cosmos_container_name = get_env_var("COSMOS_CONTAINER_NAME")

# Create clients
credential = DefaultAzureCredential()
servicebus_client = ServiceBusClient(servicebus_fqdn, credential=credential)
storage_account_client = BlobServiceClient(account_url=storage_account_url, credential=credential)
cosmos_client = CosmosClient(cosmos_account_url, credential=credential)
cosmos_database = cosmos_client.get_database_client(cosmos_db_name)
cosmos_container = cosmos_database.get_container_client(cosmos_container_name)

client = AsyncAzureOpenAI(
    api_key=azure_openai_api_key,  
    api_version=azure_openai_api_version,
    base_url=f"{azure_openai_endpoint}/openai/deployments/{azure_openai_deployment_name}"
)

async def process_message(msg, receiver):
    """
    Process a single message and then complete it.
    """
    print(f"Processing message: {msg}")
    message_body = json.loads(str(msg))
    blob_name = message_body.get("blob_name", "")
    id = message_body.get("id", "")
    blob_client = storage_account_client.get_blob_client(storage_container, blob_name)
    print(f"Downloading image data from {blob_name}")
    download_stream = await blob_client.download_blob()
    image_data = await download_stream.readall()
    encoded_image = base64.b64encode(image_data).decode("utf-8")
    print(f"Sending image {blob_name} to OpenAI...")
    response = await client.chat.completions.create(
        model=azure_openai_deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": [
                {"type": "text", "text": "Describe this picture:"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
            ]}
        ]
    )
    print("OpenAI response:", f"{response.choices[0].message.content[:50]}...")
    print(f"Saving response to Cosmos DB to document with id {id}")
    doc = {
        "id": id,
        "ai_response": response.choices[0].message.content
    }
    await cosmos_container.upsert_item(doc)
    await receiver.complete_message(msg)

async def main():
    async with ServiceBusClient(servicebus_fqdn, credential=credential) as sb_client:
        receiver = sb_client.get_queue_receiver(
            queue_name=servicebus_queue,
            max_lock_renewal_duration=120
        )
        async with receiver:
            while True:
                messages = await receiver.receive_messages(max_message_count=batch_size, max_wait_time=max_wait_time)
                tasks = []
                for message in messages:
                    tasks.append(asyncio.create_task(process_message(message, receiver)))
                if tasks:
                    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())