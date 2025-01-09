import os
import time
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import gradio as gr
from azure.ai.inference.models import AssistantMessage, UserMessage, SystemMessage
from azure.monitor.opentelemetry import configure_azure_monitor

load_dotenv()

application_insights_connection_string = os.getenv("APPLICATION_INSIGHTS_CONNECTION_STRING", '')
if not application_insights_connection_string:
    raise Exception("An Application Insights connection string should be provided to enable monitoring")

configure_azure_monitor(connection_string=application_insights_connection_string)

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
    messages = [SystemMessage(content="You are a helpful assistant.")]
    for msg in history:
        if msg["role"] == "user":
            messages.append(UserMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AssistantMessage(content=msg["content"]))
    messages.append(UserMessage(content=message))
    
    payload = {
      "messages": messages,
      "max_tokens": 2048,
      "temperature": 0.8,
      "top_p": 0.1,
      "presence_penalty": 0,
      "frequency_penalty": 0
    }
    response = client.complete(stream=True, **payload)
    assistant_message = {"role": "assistant", "content": ""}
    
    for update in response:
        assistant_message["content"] += update.choices[0].delta.content or ""
        yield [assistant_message]

iface = gr.ChatInterface(fn=chat_interface, type="messages")
iface.launch(server_name='0.0.0.0', ssr_mode=True)
