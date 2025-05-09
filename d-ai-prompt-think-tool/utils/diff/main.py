import os
import json
from diff_match_patch import diff_match_patch
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

# Define structured output model for LLM
class Change(BaseModel):
    StartPositionMatch: str
    EndPositionMatch: str
    ChangedText: str

class Changes(BaseModel):
    changes: list[Change]

# Function to load environment variables from .env file
# Load environment variables from .env file
load_dotenv()

input_file = "./input.md"
result_file = "./output.md"
patch_file = "./patch.json"

dmp = diff_match_patch()

with open(input_file, "r", encoding="utf-8") as f:
    input_text = "\n".join(line.rstrip() for line in f)

# Retrieve patch text from Azure OpenAI with EntraAD authentication
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

# Prepare system prompt and chat_prompt per AzureOpenAI example
system_prompt = """
You are a computer scientist.
When given a document, apply the requested edits and output only differences in following format.

Strictly follow format of JSON structure which is array of objects (changes) with following fields:
- StartPositionMatch: Value containing exact match of 100 characters preceding the change
- EndPositionMatch: Value containing exact match of 100 characters following the change
- ChangedText: Value containing the change itself
"""

user_prompt = f"""
Add subtitle to each ## level chapter. Make sure it is in italics and put two \n before and after it.

<document>
{input_text}
</document>
"""

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
]

completion = client.beta.chat.completions.parse(
    model=deployment,
    messages=messages,
    max_tokens=8000,
    temperature=0,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    response_format=Changes,
)

# Parse structured output directly into Pydantic models
changes = Changes.model_validate(completion.choices[0].message.parsed)

# Persist the raw changes to disk
with open(patch_file, "w", encoding="utf-8") as pf:
    pf.write(changes.model_dump_json(indent=2))

# Print the number of changes
print(f"Total changes to apply: {len(changes.changes)}")

# Apply structured changes to the input_text as one giant string
text = input_text
# Apply changes in reverse order based on their position to avoid shifting indices
for idx, change in enumerate(changes.changes, 1):
    start_match = change.StartPositionMatch
    end_match = change.EndPositionMatch
    # find start and end indices
    start_index = text.find(start_match)
    if start_index == -1:
        raise ValueError(f"StartPositionMatch not found: {start_match}")
    start_index += len(start_match)
    end_index = text.find(end_match, start_index)
    if end_index == -1:
        raise ValueError(f"EndPositionMatch not found: {end_match}")
    # print truncated info about this change
    print(f"*** Applying change {idx}/{len(changes.changes)}: {change.ChangedText[:20]}...")
    # replace content between matches with ChangedText
    text = text[:start_index] + change.ChangedText + text[end_index:]

# Write the patched document
with open(result_file, "w", encoding="utf-8") as f:
    f.write(text)