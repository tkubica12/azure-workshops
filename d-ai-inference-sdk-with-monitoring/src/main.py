import os
import json
import base64
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import gradio as gr
from azure.ai.inference.models import AssistantMessage, UserMessage, SystemMessage
from azure.monitor.opentelemetry import configure_azure_monitor

load_dotenv()

application_insights_connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING", '')
if not application_insights_connection_string:
    raise Exception("An Application Insights connection string should be provided to enable monitoring")

configure_azure_monitor(connection_string=application_insights_connection_string)

# Load the model configuration from .models.json or MODELS_CONFIG environment variable
config = None
if os.path.exists('.models.json'):
    with open('.models.json', 'r') as file:
        config = json.load(file)
else:
    config_base64 = os.getenv("MODELS_CONFIG", '')
    if not config_base64:
        raise Exception("Provide either .models.json file or base64-encoded JSON config")
    config_json = base64.b64decode(config_base64).decode('utf-8')
    config = json.loads(config_json)

# Create clients from the config
clients = {}
for model_name, model_attrs in config.get("models", {}).items():
    api_endpoint = model_attrs.get("endpoint")
    api_key = model_attrs.get("key")
    if api_endpoint and api_key:
        clients[model_name] = ChatCompletionsClient(
            endpoint=api_endpoint,
            credential=AzureKeyCredential(api_key)
        )

if not clients:
    raise Exception("At least one set of credentials and endpoints should be provided")

model_names = list(clients.keys())
system_message = SystemMessage(content="You are a helpful assistant.")

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            chatbot_l = gr.Chatbot(type="messages")
            model_selector_l = gr.Dropdown(choices=model_names, label="Select Model")
        with gr.Column():
            chatbot_r = gr.Chatbot(type="messages")
            model_selector_r = gr.Dropdown(choices=model_names, label="Select Model")
                
    msg = gr.Textbox()
    with gr.Row():
        send = gr.Button("Send")
        clear = gr.ClearButton([msg, chatbot_l, chatbot_r])

    def user(user_message, history):
        return "", history + [{"role": "user", "content": user_message}]

    def bot_l(history, model_name):
        print(f"Model: {model_name}, History: {history}")
        messages = [system_message]
        for msg in history:
            if msg["role"] == "user":
                messages.append(UserMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AssistantMessage(content=msg["content"]))
        
        payload = {
            "messages": messages,
            "max_tokens": 2048,
            "temperature": 0.8,
            "top_p": 0.1,
            "presence_penalty": 0,
            "frequency_penalty": 0
        }
        
        client = clients.get(model_name)
        if not client:
            raise Exception(f"Client for model {model_name} not found")
        
        response = client.complete(stream=True, **payload)
        assistant_message = {"role": "assistant", "content": ""}
        for update in response:
            assistant_message["content"] += update.choices[0].delta.content or ""
            yield history + [assistant_message]

    def bot_r(history, model_name):
        print(f"Model: {model_name}, History: {history}")
        messages = [system_message]
        for msg in history:
            if msg["role"] == "user":
                messages.append(UserMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AssistantMessage(content=msg["content"]))
        
        payload = {
            "messages": messages,
            "max_tokens": 2048,
            "temperature": 0.8,
            "top_p": 0.1,
            "presence_penalty": 0,
            "frequency_penalty": 0
        }
        
        client = clients.get(model_name)
        if not client:
            raise Exception(f"Client for model {model_name} not found")
        
        response = client.complete(stream=True, **payload)
        assistant_message = {"role": "assistant", "content": ""}
        for update in response:
            assistant_message["content"] += update.choices[0].delta.content or ""
            yield history + [assistant_message]

    msg.submit(user, [msg, chatbot_l], [msg, chatbot_l], queue=False).then(
        bot_l, [chatbot_l, model_selector_l], [chatbot_l]
    )
    msg.submit(user, [msg, chatbot_r], [msg, chatbot_r], queue=False).then(
        bot_r, [chatbot_r, model_selector_r], [chatbot_r]
    )
    send.click(user, [msg, chatbot_l], [msg, chatbot_l], queue=False).then(
        bot_l, [chatbot_l, model_selector_l], [chatbot_l]
    )
    send.click(user, [msg, chatbot_r], [msg, chatbot_r], queue=False).then(
        bot_r, [chatbot_r, model_selector_r], [chatbot_r]
    )
    clear.click(lambda: [None, None], None, [chatbot_l, chatbot_r], queue=False)

demo.launch(server_name='0.0.0.0', ssr_mode=False)
