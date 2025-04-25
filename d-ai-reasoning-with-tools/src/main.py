from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
import os

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
MODEL_NAME = os.getenv("MODEL_NAME")

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = AZURE_OPENAI_ENDPOINT, 
  azure_ad_token_provider=token_provider,
  api_version="2025-03-01-preview"
)

def get_next_item(current_item):
    """
    Returns the next item in the static chain of cities to visit.
    Special items:
      - '<START>': returns the first item in the chain.
      - '<END>': returned if there is no next item.
    """
    chain = ["Prague", "Vienna", "Tokyo", "Bangkok", "Paris"]
    if current_item == "<START>":
        return chain[0]
    try:
        idx = chain.index(current_item)
        if idx + 1 < len(chain):
            return chain[idx + 1]
        else:
            return "<END>"
    except ValueError:
        return "<END>"

response = None
response_id = None
try:
    response = client.responses.create(
        model=MODEL_NAME, 
        input="This is a test.",
        stream=True
    )
    for event in response:
        if response_id is None and hasattr(event, "response_id"):
            response_id = event.response_id
        if event.type == 'response.output_text.delta':
            print(event.delta, end='', flush=True)
finally:
    if response_id is not None:
        client.responses.delete(response_id)