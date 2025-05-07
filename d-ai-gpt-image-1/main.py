import requests
import base64
import os
import time 
from dotenv import load_dotenv

load_dotenv()

# Define the prompt and other parameters
prompt = "Photorealistic detailed double portrait of wooden boxed-head robot in black hoodie with thin woman coder with thick glasses with yellow hoodie. Picture taken futuristic office, very cinematic and hyper-realistic, 2.0f."
size = "1024x1536"         # Options: "1536x1024", "1024x1536", "1024x1024"
quality = "high"           # Options: "high", "medium", "low"
background = "opaque"      # Options: "transparent", "opaque", "auto"
batch_size = 2             # Number of images to generate per variant
variants = 10               # Number of prompt variants
prefix = "medal"           # Prefix for output filenames
folder = "images"          # Folder to save images
max_retries = 15           # max attempts for image generation
backoff_factor = 3         # base seconds for exponential backoff

# Ensure output folder exists
os.makedirs(folder, exist_ok=True)

# API endpoints and headers
url = os.getenv("AZURE_API_URL")
headers = {
    "Content-Type": "application/json",
    "api-key": os.getenv("AZURE_API_KEY")
}
llm_url = os.getenv("AZURE_LLM_API_URL")
llm_headers = {
    "Content-Type": "application/json",
    "api-key": os.getenv("AZURE_LLM_API_KEY")
}

def get_prompt_variant(base_prompt, variant_num):
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that revises image-generation prompts by enhancing it, be more descriptive, try various modifications and versions."},
            {"role": "user", "content": f"Original prompt: \"{base_prompt}\". Produce a significantly altered version for variant {variant_num}."}
        ],
        "n": 1,
        "temperature": 1.0
    }
    resp = requests.post(llm_url, headers=llm_headers, json=payload)
    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"].strip()
    else:
        print(f"LLM variant {variant_num} failed: {resp.text}")
        return base_prompt

# Build all variant prompts (first is unchanged)
variant_prompts = [
    prompt if i == 1 else get_prompt_variant(prompt, i)
    for i in range(1, variants + 1)
]

# Generate images for each variant
for v_num, var_prompt in enumerate(variant_prompts, start=1):
    print(f"\nVariant v{v_num} prompt:\n{var_prompt}\n")
    data = {
        "prompt": var_prompt,
        "size": size,
        "quality": quality,
        "n": batch_size,
        "background": background
    }
    # new: attempt POST with retries on 429/5xx
    resp = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(url, headers=headers, json=data)
            # success if not rate‑limited or server error
            if resp.status_code < 500 and resp.status_code != 429:
                break
            raise Exception(f"Status {resp.status_code}")
        except Exception as e:
            if attempt == max_retries:
                print(f"Variant v{v_num}: all {max_retries} attempts failed: {e}")
            else:
                wait = backoff_factor * (2 ** (attempt - 1))
                print(f"Variant v{v_num}: attempt {attempt} failed ({e}), retrying in {wait}s…")
                time.sleep(wait)

    # Check for successful response
    if resp and resp.status_code == 200:
        images = resp.json()["data"]
        for idx, item in enumerate(images, start=1):
            img_data = item["b64_json"]
            fname = f"{prefix}-v{v_num}-{idx:02d}.png"
            path = os.path.join(folder, fname)
            with open(path, "wb") as f:
                f.write(base64.b64decode(img_data))
        print(f"Variant v{v_num}: saved {len(images)} images.")
    else:
        print(f"Image generation v{v_num} failed: {resp.status_code} {resp.text}")
