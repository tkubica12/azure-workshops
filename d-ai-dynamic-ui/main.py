from fasthtml.common import Form, Input, Button, Div, P, Title, Head, Meta, Link, Body, fast_app, serve, Style, Span
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

# --- Globals for session storage (simplified) ---
latest_user_question = None
latest_ai_snippet = None
# --- End Globals ---

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
        # Form for user input
        Form(
            Input(id='user_query', name='user_query', type='text', placeholder='Enter your question here...', cls='border p-2 flex-grow rounded'),
            Button(
                Span('Send', cls='btn-text-label'),
                Span(cls='spinner-graphic'), 
                id='send-button',
                type='submit', 
                cls='bg-blue-500 text-white p-2 rounded ml-2 flex items-center justify-center relative w-[100px] h-[40px]' 
            ),
            hx_post='/userMessage',
            hx_target='#ai-output',
            hx_swap='innerHTML',  # Replace the content of ai-output
            hx_indicator='#send-button', # Indicator is now the button itself
            cls='flex mt-4'
        ),
        cls='container mx-auto p-4'
    )
    # Basic styling using Tailwind CSS CDN
    return Title('FastHTML LLM Chat'), \
           Head(
               Meta(charset='UTF-8'),
               Link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'),
               Style('''
                 @keyframes spin {
                   to { transform: rotate(360deg); }
                 }
                 /* Styles for the spinner graphic itself */
                 .spinner-graphic {
                   display: none; /* Initially hidden */
                   width: 20px;   /* Spinner size for button */
                   height: 20px;
                   border: 3px solid rgba(255, 255, 255, 0.3); /* Lighter border for on-button */
                   border-top-color: #ffffff; /* White spinner on blue button */
                   border-radius: 50%;
                   animation: spin 0.8s linear infinite;
                 }
                 /* When the button (acting as indicator) is in htmx-request state */
                 #send-button.htmx-request .btn-text-label {
                   display: none; /* Hide text when request is active */
                 }
                 #send-button.htmx-request .spinner-graphic {
                   display: inline-block; /* Show spinner */
                 }
               ''')
           ), \
           Body(chat_container)

@rt('/userMessage')
def post(user_query: str):
    global latest_user_question, latest_ai_snippet  # Allow modification of globals
    logger.info('POST /userMessage started')
    # Load system_message template from file
    with open('prompts/system.jinja2', encoding='utf-8') as f:
        template = Template(f.read())
    # For a new user message, there's no previously generated snippet in this direct interaction
    system_message = template.render(previously_generated_snippet=None)

    latest_user_question = user_query # Store the user question

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
    
    latest_ai_snippet = content_text # Store the AI snippet
    logger.debug(f'LLM response: {content_text}')
    return content_text

@rt('/process')
def post(interaction_details: str | None = None): # Make interaction_details optional
    global latest_user_question, latest_ai_snippet # Allow access and modification of globals
    
    actual_interaction_details_for_prompt: str
    if interaction_details is None:
        # This case will be hit if the HTMX snippet doesn't send `interaction_details`
        logger.warning("POST /process: 'interaction_details' was not provided by the client. Ensure HTMX snippets use hx-vals correctly.")
        # Provide a default value for the prompt to avoid breaking the flow
        actual_interaction_details_for_prompt = "User clicked an interactive element, but specific details were not captured."
        logger.info(f'POST /process proceeding with placeholder interaction details: "{actual_interaction_details_for_prompt}"')
    else:
        logger.info(f'POST /process started with interaction: {interaction_details}')
        actual_interaction_details_for_prompt = interaction_details

    if not latest_user_question:
        logger.error('Original user question not found in session.')
        return '<div id="ai-output" class="border p-4 min-h-[200px] bg-red-100 rounded text-red-700">Error: Original question context lost. Please start a new conversation.</div>'
    if not latest_ai_snippet:
        logger.error('Previously generated AI snippet not found in session.')
        # Potentially less critical, could try to recover or ask user to clarify
        return '<div id="ai-output" class="border p-4 min-h-[200px] bg-yellow-100 rounded text-yellow-700">Warning: Previous AI response context lost. The AI might not fully understand the interaction.</div>'

    # Load system_message template
    with open('prompts/system.jinja2', encoding='utf-8') as f:
        system_template = Template(f.read())
    system_message = system_template.render(previously_generated_snippet=latest_ai_snippet)

    # Load user_interaction_prompt template
    with open('prompts/user_interaction_prompt.jinja2', encoding='utf-8') as f:
        user_interaction_template = Template(f.read())
    
    user_prompt_content = user_interaction_template.render(
        original_user_question=latest_user_question,
        interaction_details=actual_interaction_details_for_prompt # Use the potentially defaulted value
    )

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt_content}
    ]

    logger.info('Sending data to LLM for /process')
    try:
        response = client.responses.create(
            model=MODEL_NAME,
            input=messages,
            reasoning={
                "effort": "low",
                "summary": "detailed",
            },
        )
        logger.info('Received response from LLM for /process')
        logger.debug(f'LLM full response: {response}')

        content_text = None
        for item in response.output:
            if getattr(item, 'type', None) == 'message' and hasattr(item, 'content'):
                content_text = item.content[0].text
                break
        
        if not content_text:
            logger.error('No message output found in LLM response for /process')
            return '<div id="ai-output" class="border p-4 min-h-[200px] bg-red-100 rounded text-red-700">Error: No message output found in LLM response.</div>'

        latest_ai_snippet = content_text # Update the latest AI snippet
        logger.debug(f'LLM response for /process: {content_text}')
        return content_text

    except Exception as e:
        logger.error(f'Error during LLM call in /process: {e}')
        return f'<div id="ai-output" class="border p-4 min-h-[200px] bg-red-100 rounded text-red-700">Error processing your request: {str(e)}</div>'

logger.info('Starting FastHTML app')
serve()