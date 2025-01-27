import os
import dotenv
from azure.servicebus import ServiceBusClient
from azure.identity import DefaultAzureCredential
from concurrent.futures import ThreadPoolExecutor
import json
from azure.storage.blob import BlobClient, BlobServiceClient
import requests
import base64
from openai import AzureOpenAI
# import logging

# logging.basicConfig(level=logging.INFO)

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

# Create clients
credential = DefaultAzureCredential()
servicebus_client = ServiceBusClient(servicebus_fqdn, credential=credential)
storage_account_client = BlobServiceClient(account_url=storage_account_url, credential=credential)

client = AzureOpenAI(
    api_key=azure_openai_api_key,  
    api_version=azure_openai_api_version,
    base_url=f"{azure_openai_endpoint}/openai/deployments/{azure_openai_deployment_name}"
)

def process_message(msg, receiver):
    """
    Process a single message and then complete it.
    """
    print(f"Processing message: {msg}")
    message_body = json.loads(str(msg))
    blob_name = message_body.get("blob_name", "")
    blob_client = storage_account_client.get_blob_client(storage_container, blob_name)
    print(f"Downloading image data from {blob_name}")
    image_data = blob_client.download_blob().readall()
    encoded_image = base64.b64encode(image_data).decode("utf-8")
    print(f"Sending image {blob_name} to OpenAI...")
    response = client.chat.completions.create(
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
    receiver.complete_message(msg)

def main():
    """
    Main entry point. Continuously receives messages in batches,
    prints them, and completes them after processing.
    """
    with servicebus_client:
        receiver = servicebus_client.get_queue_receiver(
            queue_name=servicebus_queue,
            max_lock_renewal_duration=120 
        )
        messages = receiver.receive_messages(max_message_count=5, max_wait_time=2)
        for message in messages:
            process_message(message, receiver)

        # with ThreadPoolExecutor(max_workers=5) as executor:
        #     while True:
        #         messages = receiver.receive_messages(max_message_count=5, max_wait_time=2)
        #         for message in messages:
        #             executor.submit(process_message, message, receiver)

if __name__ == "__main__":
    main()