import os
import json
from diff_match_patch import diff_match_patch
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI
from pydantic import BaseModel
from enum import Enum
from dotenv import load_dotenv
from typing import List

# Define structured output model for LLM
class ChangeType(Enum):
    ADD = "add"
    REMOVE = "remove"
    REPLACE = "replace"

class Change(BaseModel):
    LineNum: int  # changed from str to int
    NewLine: str
    ChangeType: ChangeType

class Changes(BaseModel):
    changes: list[Change]

# Function to load environment variables from .env file
# Load environment variables from .env file
load_dotenv()

input_file = "../../outputs/document_explicit_prompt.md"
# input_file = "./input.md"
result_file = "./output.md"
patch_file = "./patch.json"

dmp = diff_match_patch()

# ---------- 1. Load input (keep raw + numbered variants) ----------
with open(input_file, "r", encoding="utf-8") as f:
    original_lines: List[str] = [line.rstrip("\n") for line in f]           # raw text to be patched

numbered_lines = [f"{i+1:04d}: {l}" for i, l in enumerate(original_lines)]  # view for LLM
numbered_text = "\n".join(numbered_lines)

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

# ---------- 2. Build system & user prompts ----------
system_prompt = """
You are a computer scientist.
When given a line-numbered document, output JSON describing edits.

Each JSON element MUST have:
- "LineNum": 4-digit string reflecting the line to operate on
- "NewLine": resulting line (omit or leave empty for removals)
- "ChangeType": one of "add", "remove", "replace"

Do NOT include the line numbers in NewLine.
"""

user_prompt = f"""
The document lines are prefixed with "####: " numbers – do not change these prefixes.

Task:
Add an italic subtitle to every '## ' level heading.
Insert blank line before and after that subtitle.

Return only the JSON array described above.

<document>
{numbered_text}
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

# ---------- 3. Apply patch bottom-up ----------
patched_lines = original_lines.copy()

# sort by line number descending so indexes stay valid while mutating
for ch in sorted(changes.changes, key=lambda c: c.LineNum, reverse=True):
    idx = ch.LineNum - 1
    if ch.ChangeType == ChangeType.ADD:
        patched_lines.insert(idx + 1, ch.NewLine)
    elif ch.ChangeType == ChangeType.REMOVE:
        if 0 <= idx < len(patched_lines):
            patched_lines.pop(idx)
    elif ch.ChangeType == ChangeType.REPLACE:
        if 0 <= idx < len(patched_lines):
            patched_lines[idx] = ch.NewLine

patched_text = "\n".join(patched_lines) + "\n"

# ---------- 4. Persist patched document ----------
with open(result_file, "w", encoding="utf-8") as f:
    f.write(patched_text)