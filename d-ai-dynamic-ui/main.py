from fasthtml.common import Form, Input, Button, Div, P, Title, Head, Meta, Link, Body, fast_app, serve, Style
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
import os
from jinja2 import Template
import logging

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Define the FastHTML app
app, rt = fast_app()

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
  api_version="2025-04-01-preview"
)

@rt('/')
def get():
    # Main container for the chat interface
    chat_container = Div(
        # Large element for AI output
        Div(id='ai-output', cls='border p-4 min-h-[200px] bg-gray-100 rounded', innerHTML=P('AI responses will appear here.')),
        # Loading indicator - now a spinner
        Div(id='loading-indicator', cls='htmx-indicator spinner-container'),
        # Form for user input
        Form(
            Input(id='user_query', name='user_query', type='text', placeholder='Enter your question here...', cls='border p-2 flex-grow rounded'),
            Button('Send', type='submit', cls='bg-blue-500 text-white p-2 rounded ml-2'),
            hx_post='/userMessage',
            hx_target='#ai-output',
            hx_swap='innerHTML',  # Replace the content of ai-output
            hx_indicator='#loading-indicator', # Show loading indicator during request
            cls='flex mt-4'
        ),
        cls='container mx-auto p-4'
    )
    # Basic styling using Tailwind CSS CDN
    return Title('FastHTML LLM Chat'), \
           Head(
               Meta(charset='UTF-8'), # Corrected charset from UTF-S to UTF-8
               Link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'),
               Style('''
                 .htmx-indicator {
                   display: none;
                 }
                 .htmx-indicator.htmx-request {
                   display: flex; /* Changed to flex for centering spinner */
                   justify-content: center;
                   align-items: center;
                   padding: 10px; /* Add some padding around the spinner */
                 }
                 .spinner-container::after {
                   content: "";
                   display: block;
                   width: 40px; /* Spinner size */
                   height: 40px; /* Spinner size */
                   border-radius: 50%;
                   border: 4px solid #f3f3f3; /* Light grey border */
                   border-top-color: #3498db; /* Blue color for spinner */
                   animation: spin 1s linear infinite;
                 }
                 @keyframes spin {
                   to { transform: rotate(360deg); }
                 }
               ''')
           ), \
           Body(chat_container)

@rt('/userMessage')
def post(user_query: str):
    logger.info('POST /userMessage started')
    # Load system_message template from file
    with open('prompts/system.jinja2', encoding='utf-8') as f:
        template = Template(f.read())
    system_message = template.render()

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_query}
    ]

    logger.info('Sending data to LLM')
    # Call the Azure OpenAI model
    response = client.responses.create(
        model=MODEL_NAME,
        input=messages,
        reasoning={
            "effort":  "low",         # optional: low | medium | high
            "summary": "detailed",      # auto | concise | detailed
        },
    )
    logger.info('Received response from LLM')
    logger.debug(f'LLM full response: {response}')

    content_text = None
    try:
        for item in response.output:
            if getattr(item, 'type', None) == 'message' and hasattr(item, 'content'):
                content_text = item.content[0].text
                break
    except Exception as e:
        logger.error(f'Could not extract content text from LLM response: {e}')
        return 'Error: Could not extract content from LLM response.'
    if not content_text:
        logger.error('No message output found in LLM response')
        return 'Error: No message output found in LLM response.'
    logger.debug(f'LLM response: {content_text}')
    return content_text

logger.info('Starting FastHTML app')
serve()