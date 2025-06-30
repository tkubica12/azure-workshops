# Local LLM Service

A FastAPI-based service for running Gemma 2 2B model locally with efficient resource management.

## Features

- **Independent Lifecycle**: Runs separately from the main Reflex application
- **Efficient Resource Management**: Model loads once and stays in memory
- **RESTful API**: Clean HTTP API for token generation and service monitoring
- **Quantization Support**: 4-bit quantization for memory efficiency (~75% reduction)
- **Health Monitoring**: Built-in health checks and status endpoints
- **Docker Support**: Containerized deployment ready

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment (optional)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file or set environment variables:

```bash
# Required
HUGGINGFACE_TOKEN=your_hf_token_here

# Optional (with defaults)
LOCAL_MODEL_NAME=google/gemma-2-2b
DEVICE=auto
USE_QUANTIZATION=true
LLM_SERVICE_HOST=0.0.0.0
LLM_SERVICE_PORT=8001
```

### 3. Start the Service

```bash
# Using the startup script
python start_service.py

# Or directly with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

The service will be available at `http://localhost:8001`

## API Endpoints

### Health Check
```bash
GET /health
```

### Service Status
```bash
GET /api/v1/status
```

### Test Generation
```bash
POST /api/v1/test
```

### Token Generation
```bash
POST /api/v1/generate
{
  "prompt": "The capital of France is",
  "max_tokens": 1,
  "temperature": 0.7,
  "top_logprobs": 5
}
```

## Docker Deployment

```bash
# Build image
docker build -t llm-service .

# Run container
docker run -p 8001:8001 --env-file .env llm-service
```

## Development

### Running Tests

```bash
python test_service.py
```

### Configuration Options

See `config/settings.py` for all available configuration options.

## Resource Requirements

- **Memory**: 8GB+ RAM (4GB+ with quantization)
- **GPU**: Optional but recommended (CUDA-compatible)
- **Storage**: ~5GB for model cache

## Troubleshooting

1. **Model loading fails**: Check Hugging Face token and internet connection
2. **CUDA errors**: Ensure CUDA drivers are installed or set `DEVICE=cpu`
3. **Memory issues**: Enable quantization with `USE_QUANTIZATION=true`
