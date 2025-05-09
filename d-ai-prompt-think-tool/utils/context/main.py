import os
import json
import requests
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

llmstxt_url = "https://www.mux.com/llms-full.txt"
output_file = "../../outputs/document_with_context.md"

# Download the file content
print("Downloading Vue.js documentation...")
response = requests.get(llmstxt_url)
response.raise_for_status()
documentation_text = response.text

system_prompt = f"""
# Role
You are computer scientist teacher with 10 years of experience and ability to explain complex concepts in simple terms.

# Instructions
- If you use any jargon or technical terms, explain them.
- Use examples to illustrate your points.
- Use analogies to make the concepts relatable.
- Provide a summary at the end to reinforce learning.
- Keep the tone friendly and engaging.
- Use markdown formatting for better readability.
- Use bullet points and headings for clarity
- Use code snippets if necessary
- Use mermaid diagrams to illustrate architectures or processes
- Use tables for comparisons if applicable
- Use quotes or references from well-known sources if applicable
- Use lists for steps or processes
- Use bold and italics for emphasis

# Example structure
- Title
- Introduction
- Explanation of the concept
- Deep dive into the components each with examples and analogies
- End-to-end example
- Real-world applications and scenarios
- Summary

# Context
Make sure all your outputs are based on the context provided.
Here is complete documentation of Vue.js for your reference:
<documentation>
{documentation_text}
</documentation>
"""

user_prompt = "How to do audio normalization in Mux?"

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("MODEL_NAME")
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)
client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2025-01-01-preview",
)

print("Generating response...")

completion = client.beta.chat.completions.parse(
    model=deployment,
    messages=messages,
    max_tokens=30000,
    temperature=0,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(completion.choices[0].message.content)


