from fasthtml.common import Form, Input, Button, Div, P, Title, Head, Meta, Link, Body, fast_app, serve

app, rt = fast_app()

@rt('/')
def get():
    # Main container for the chat interface
    chat_container = Div(
        # Large element for AI output
        Div(id='ai-output', cls='border p-4 min-h-[200px] bg-gray-100 rounded', innerHTML=P('AI responses will appear here.')),
        # Form for user input
        Form(
            Input(id='user_query', name='user_query', type='text', placeholder='Enter your question here...', cls='border p-2 flex-grow rounded'),
            Button('Send', type='submit', cls='bg-blue-500 text-white p-2 rounded ml-2'),
            hx_post='/userMessage',
            hx_target='#ai-output',
            hx_swap='innerHTML',  # Replace the content of ai-output
            cls='flex mt-4'
        ),
        cls='container mx-auto p-4'
    )
    # Basic styling using Tailwind CSS CDN
    return Title('FastHTML LLM Chat'), \
           Head(
               Meta(charset='UTF-8'),
               Link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css')
           ), \
           Body(chat_container)

@rt('/userMessage')
def post(user_query: str):
    # In a real application, you would call your LLM here with user_query.
    # For example: ai_response_htmx = call_llm_and_format_response(user_query)

    # Simulate an AI response as HTMX.
    # This HTMX will replace the content of the #ai-output div.
    ai_response_htmx = Div(
        P(f'You asked: {user_query}'),
        P('AI says: This is a simulated response from the LLM. In a real app, this would be dynamic HTMX.'),
        cls='border p-4 min-h-[200px] bg-gray-100 rounded' # Maintain styling
    )
    return ai_response_htmx

serve()