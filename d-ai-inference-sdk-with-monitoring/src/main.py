import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

api_key = os.getenv("AZURE_INFERENCE_CREDENTIAL", '')
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

api_endpoint = os.getenv("AZURE_INFERENCE_ENDPOINT", '')
if not api_endpoint:
    raise Exception("An endpoint should be provided to invoke the endpoint")

client = ChatCompletionsClient(
    endpoint=api_endpoint,
    credential=AzureKeyCredential(api_key)
)

def chat_interface(message, history):
    payload = {
      "messages": history + [
        {
          "role": "user",
          "content": message
        }
      ],
      "max_tokens": 2048,
      "temperature": 0.8,
      "top_p": 0.1,
      "presence_penalty": 0,
      "frequency_penalty": 0
    }
    response = client.complete(payload)
    assistant_message = {
        "role": "assistant",
        "content": response.choices[0].message.content
    }
    return history + [assistant_message]

iface = gr.ChatInterface(fn=chat_interface, type="messages")
iface.launch()
