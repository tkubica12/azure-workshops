from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
import os
import json
import itertools

# Load environment variables from .env file
load_dotenv()

# Get Azure OpenAI endpoint and model name from environment variables
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
MODEL_NAME = os.getenv("MODEL_NAME")

# Set up Azure AD token provider for authentication
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

# Initialize Azure OpenAI client
client = AzureOpenAI(
  azure_endpoint = AZURE_OPENAI_ENDPOINT, 
  azure_ad_token_provider=token_provider,
  api_version="2025-03-01-preview"
)

# Tool that model can use, it is static for demo purposes
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

# Define available tools for the model
tools = [{
    "type": "function",
    "name": "get_next_item",
    "description": "Returns the next city in the chain of cities to visit",
    "parameters": {
        "type": "object",
        "properties": {
            "current_item": {
                "type": "string",
                "description": "The current city. Use '<START>' to get the first city."
            }
        },
        "required": ["current_item"],
        "additionalProperties": False
    }
}]

# Initialize response tracking variables
response_id = None
input_messages = [{"role": "user", "content": "Gather full chain of cities to visit."}]

# Loop until the model stops calling tools
while True: 
    # Create a streaming response from the model
    response = client.responses.create(
        model=MODEL_NAME,
        input=input_messages,
        tools=tools,
        stream=True
    )

    # Collect tool outputs to send back after this streaming pass
    pending_outputs = []

    # Process streaming events from the model
    for event in response:
        if hasattr(event, "response_id"):
            response_id = event.response_id
        if event.type == 'response.output_text.delta':
            print(event.delta, end='', flush=True)
        elif event.type == 'response.function_call_arguments.delta':
            print(event.delta, end='', flush=True)
        elif event.type == 'response.output_item.added':
            if event.item.type == 'function_call':
                print(f"\n### Calling {event.item.name}, arguments: ", end='', flush=True)
            elif event.item.type == 'reasoning':
                print(f"\n$$$ Reasoning $$$")
            elif event.item.type == 'message':
                print("*** Responding ***")
            else:
                print(f"[DEBUG] Added item: {event.item}")
        elif event.type == 'response.output_item.done':
            if event.item.type == 'function_call' and event.item.name == 'get_next_item':
                # 1. Execute tool
                current_item = json.loads(event.item.arguments)['current_item']
                next_item = get_next_item(current_item)
                print(f"\n### Function call result: {next_item}")

                # 2. Remember messages to send back in next request
                input_messages.append(event.item)                  # the call itself
                pending_outputs.append({                           # its result
                    "type": "function_call_output",
                    "call_id": event.item.call_id,
                    "output": next_item
                })
            elif event.item.type == 'reasoning':
                print("$$$ Finished reasoning. $$$")
                input_messages.append(event.item)    # keep reasoning in history
            elif event.item.type == 'message':
                print("\n\n*** Finished responding. ***")
            else:
                print(f"\n[DEBUG] Done item: {event.item}")        
    # After stream ends, append all outputs (if any) and decide whether to loop again
    if not pending_outputs:
        break                                   # no more tool calls → finished
    input_messages.extend(pending_outputs)      # add results, then loop

# Cleanup: delete the response if it exists
if response_id is not None:
    client.responses.delete(response_id)