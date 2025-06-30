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

This project uses uv for dependency management with support for both CPU and GPU PyTorch variants.

#### Using uv (Recommended)

```bash
# Install uv if not already installed
pip install uv

# For CPU development/deployment
uv sync --extra cpu

# For GPU development/deployment (Windows/Linux with CUDA 12.8)
uv sync --extra gpu-cuda128

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
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

### Quick Start with Build Scripts

#### Linux/macOS
```bash
# Make script executable
chmod +x build.sh

# Build CPU image
./build.sh

# Build GPU image
./build.sh --target gpu

# Build both images
./build.sh --target all
```

#### Windows
```powershell
# Build CPU image
.\build.ps1

# Build GPU image
.\build.ps1 -Target gpu

# Build both images
.\build.ps1 -Target all
```

### Using Docker Compose (Recommended)

#### CPU Version (Default)
```bash
# Copy environment file
cp .env.example .env
# Edit .env with your HUGGINGFACE_TOKEN

# Run CPU version
docker-compose --profile cpu up -d

# View logs
docker-compose logs -f llm-service-cpu
```

#### GPU Version
```bash
# Ensure nvidia-docker is installed
# Copy environment file
cp .env.example .env
# Edit .env with your HUGGINGFACE_TOKEN

# Run GPU version
docker-compose --profile gpu up -d

# View logs
docker-compose logs -f llm-service-gpu
```

### Using Docker Directly

#### CPU Version
```bash
# Build CPU image
docker build -t llm-service:cpu .

# Run CPU container
docker run -p 8001:8001 --env-file .env llm-service:cpu
```

#### GPU Version
```bash
# Build GPU image
docker build -f Dockerfile.gpu -t llm-service:gpu .

# Run GPU container (requires nvidia-docker)
docker run --gpus all -p 8001:8001 --env-file .env llm-service:gpu
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
