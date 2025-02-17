import os  
import time  # added import
import math  # added import
from openai import AzureOpenAI  
from azure.identity import DefaultAzureCredential, get_bearer_token_provider  
from dotenv import load_dotenv
from azure.monitor.opentelemetry import configure_azure_monitor
from azure.core.settings import settings
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor

# Load environment variables
load_dotenv()
endpoint = os.getenv("ENDPOINT_URL")  
deployment = os.getenv("DEPLOYMENT_NAME")  
subscription_key = os.getenv("SUBSCRIPTION_KEY")
# appinsights_connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

# # Configure Azure Monitor - does not currently work as OpenAI SDK implements this only in newer version, not legacy one. But legacy is used in this demo to access to raw headers which is not yet available in newer version of OpenAI SDK.
# resource = Resource.create({SERVICE_NAME: "AI Worker Service"})
# configure_azure_monitor(connection_string=appinsights_connection_string, resource=resource)
# settings.tracing_implementation = "opentelemetry"
# OpenAIInstrumentor().instrument()
      
# Initialize Azure OpenAI Service client with Entra ID authentication
token_provider = get_bearer_token_provider(  
    DefaultAzureCredential(),  
    "https://cognitiveservices.azure.com/.default"  
)  
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    azure_ad_token_provider=token_provider,  
    api_version="2024-05-01-preview", 
    max_retries=20,
    default_headers = {"Ocp-Apim-Subscription-Key": subscription_key}
)  

# Initialize counters for tokens calculation
total_token_usage = 0
backend_tokens = {}

# Start timing
start_time = time.time()  # added start time

# Function to print running statistics
def print_running_stats(total_token_usage, backend_tokens, start_time, request_start_time):
    elapsed_seconds_running = time.time() - start_time
    elapsed_minutes_running = math.ceil(elapsed_seconds_running / 60) 
    request_elapsed_seconds = time.time() - request_start_time
    tokens_per_minute_running = total_token_usage / elapsed_minutes_running
    print(f"Running total tokens: {total_token_usage}")
    print(f"Running tokens per minute: {int(tokens_per_minute_running)}")
    print(f"Request time: {request_elapsed_seconds:.2f} seconds")
    print("Tokens per backend so far:")
    for url, tokens in backend_tokens.items():
        print(f"  {url}: {tokens}")

test_messages = [
    "Hello!",
    "How can I open Word document in Windows 11?",
    "What is data quality management good for in context of IT?",
    "Give me advantages of using data quality management.",
    "What are reasons for using data quality management?",
    "Write long text about life, universe and everything.",
    "Write long text about life, universe and everything.",
    "Write long text about life, universe and everything, please.",
    "Write text about life, universe and everything.",
    "Write long text about life, universe, and everything.",
]

for message in test_messages:
    messages = [  
        {  
            "role": "system",  
            "content": "You are a helpful assistant."  
        },  
        {  
            "role": "user",  
            "content": message
        }  
    ]

    request_start_time = time.time()
    response = client.chat.completions.with_raw_response.create(  
        model=deployment,  
        messages=messages,
        max_tokens=1000,  
        temperature=0.7,  
        top_p=0.95,  
        frequency_penalty=0,  
        presence_penalty=0,
        stop=None,  
        stream=False  
    )  

    response_parsed = response.parse()
    current_tokens = response_parsed.usage.total_tokens
    total_token_usage += current_tokens

    backend_url = response.headers.get('x-openai-backendurl')
    if backend_url in backend_tokens:
        backend_tokens[backend_url] += current_tokens
    else:
        backend_tokens[backend_url] = current_tokens
    
    response_text_shortened = response_parsed.choices[0].message.content[:80].replace("\n", " ") + "..." 
    print(f"\nResponse {current_tokens} tokens: {response_text_shortened}")
    print(f"x-openai-backendurl: {backend_url}")
    print_running_stats(total_token_usage, backend_tokens, start_time, request_start_time)

# Print final statistics
print("\n-----------------------------------")
print("Final stats:")
print_running_stats(total_token_usage, backend_tokens, start_time, start_time)

