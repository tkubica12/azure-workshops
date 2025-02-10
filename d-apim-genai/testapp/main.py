import os  
from openai import AzureOpenAI  
from azure.identity import DefaultAzureCredential, get_bearer_token_provider  
from dotenv import load_dotenv

load_dotenv()
        
endpoint = os.getenv("ENDPOINT_URL", "https://p1-apim-genai-rytf.openai.azure.com/")  
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")  
subscription_key = os.getenv("SUBSCRIPTION_KEY")
      
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

test_messages = [
    "Hello!",
    "How can I open Word document in Windows 11?",
    "What is data quality management good for in context of IT?",
    "Write long text about life, universe and everything.",
    "Write long text about life, universe and everything.",
    "Write long text about life, universe and everything.",
    "Write long text about life, universe and everything.",
    "Write long text about life, universe and everything.",
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
    # Print running totals
    print(f"Running total tokens: {total_token_usage}")
    print("Tokens per backend so far:")
    for url, tokens in backend_tokens.items():
        print(f"  {url}: {tokens}")

print(f"\n-----------------------------------\nFinal total token usage: {total_token_usage}")
print("Final tokens per backend:")
for url, tokens in backend_tokens.items():
    print(f"  {url}: {tokens}")

