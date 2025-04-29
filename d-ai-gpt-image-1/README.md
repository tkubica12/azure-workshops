# gpt-image-1

A Python script to generate image variants via Azure OpenAI Image and LLM APIs.

## Configuration

Create a `.env` file in the project root with the following keys:

```properties
AZURE_API_KEY=your_image_api_key
AZURE_API_URL="https://<your-endpoint>/openai/deployments/<deployment>/images/generations?api-version=2025-04-01-preview"
AZURE_LLM_API_KEY=your_llm_api_key
AZURE_LLM_API_URL="https://<your-endpoint>/openai/deployments/<deployment>/chat/completions?api-version=2025-01-01-preview"
```

## Key Variables in `main.py`

- prompt: base description for image generation  
- size: image dimensions (e.g. `1024x1024`)  
- quality: `"high"`, `"medium"`, or `"low"`  
- background: `"transparent"`, `"opaque"`, or `"auto"`  
- batch_size: images per prompt variant  
- variants: number of prompt variations  
- prefix: filename prefix for outputs  
- folder: output directory (defaults to `images/`)  
- max_retries, backoff_factor: retry logic settings  

## Running

Install dependencies and run the script:

```bash
pip install -r requirements.txt
uv run main.py
```
