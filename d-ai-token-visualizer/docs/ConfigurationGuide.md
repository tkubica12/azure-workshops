# Configuration Guide

## Overview

This guide covers all configuration options for the Token Visualizer application, including environment variables, model settings, and deployment configurations.

## Table of Contents

1. [Environment Variables](#environment-variables)
2. [Model Configuration](#model-configuration)
3. [Service Configuration](#service-configuration)
4. [Performance Tuning](#performance-tuning)
5. [Security Settings](#security-settings)
6. [Development vs Production](#development-vs-production)

---

## Environment Variables

### Main Application (.env)

**Location**: `token_visualizer/.env`

```env
# LLM Service Configuration
LLM_SERVICE_URL=http://localhost:8001
LLM_SERVICE_TIMEOUT=30
LLM_SERVICE_API_KEY=optional_api_key

# Reflex Configuration
REFLEX_LOG_LEVEL=info
REFLEX_BACKEND_PORT=8000
REFLEX_FRONTEND_PORT=3000

# Development Settings
DEBUG=false
RELOAD=false
```

**Variable Descriptions**:

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_SERVICE_URL` | `http://localhost:8001` | Base URL for LLM service API |
| `LLM_SERVICE_TIMEOUT` | `30` | Timeout in seconds for API calls |
| `LLM_SERVICE_API_KEY` | None | Optional API key for service authentication |
| `REFLEX_LOG_LEVEL` | `info` | Logging level: debug, info, warning, error |
| `REFLEX_BACKEND_PORT` | `8000` | Port for Reflex backend |
| `REFLEX_FRONTEND_PORT` | `3000` | Port for Reflex frontend |
| `DEBUG` | `false` | Enable debug mode |
| `RELOAD` | `false` | Enable auto-reload on code changes |

### LLM Service (.env)

**Location**: `llm_service/.env`

```env
# Model Configuration
MODEL_NAME=google/gemma-2-2b
MODEL_CACHE_DIR=./models
DEVICE=auto
MAX_LENGTH=2048
TORCH_DTYPE=auto

# Service Configuration
HOST=0.0.0.0
PORT=8001
LOG_LEVEL=info
WORKERS=1

# Performance Settings
BATCH_SIZE=1
USE_FLASH_ATTENTION=false
COMPILE_MODEL=false

# Memory Management
LOW_CPU_MEM_USAGE=true
LOAD_IN_8BIT=false
LOAD_IN_4BIT=false

# Authentication (Optional)
API_KEY=your_optional_api_key
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Hugging Face Configuration
HF_TOKEN=your_huggingface_token
HF_HOME=./cache/huggingface
```

**Variable Descriptions**:

| Variable | Default | Description |
|----------|---------|-------------|
| **Model Settings** | | |
| `MODEL_NAME` | `google/gemma-2-2b` | Hugging Face model identifier |
| `MODEL_CACHE_DIR` | `./models` | Local directory for model storage |
| `DEVICE` | `auto` | Device for inference: auto, cpu, cuda, cuda:0 |
| `MAX_LENGTH` | `2048` | Maximum context length |
| `TORCH_DTYPE` | `auto` | Data type: auto, float16, float32, bfloat16 |
| **Service Settings** | | |
| `HOST` | `0.0.0.0` | Host to bind service to |
| `PORT` | `8001` | Port for LLM service |
| `LOG_LEVEL` | `info` | Logging level |
| `WORKERS` | `1` | Number of worker processes |
| **Performance** | | |
| `BATCH_SIZE` | `1` | Batch size for inference |
| `USE_FLASH_ATTENTION` | `false` | Enable flash attention (if available) |
| `COMPILE_MODEL` | `false` | Compile model with torch.compile |
| **Memory** | | |
| `LOW_CPU_MEM_USAGE` | `true` | Optimize CPU memory usage |
| `LOAD_IN_8BIT` | `false` | Use 8-bit quantization |
| `LOAD_IN_4BIT` | `false` | Use 4-bit quantization |
| **Security** | | |
| `API_KEY` | None | Optional API key authentication |
| `ALLOWED_ORIGINS` | `*` | CORS allowed origins |
| **Hugging Face** | | |
| `HF_TOKEN` | None | Hugging Face authentication token |
| `HF_HOME` | `./cache/huggingface` | Hugging Face cache directory |

---

## Model Configuration

### Supported Models

**Primary Model**:
- **google/gemma-2-2b**: Main model, balanced performance and size
- **Size**: ~4.5GB download
- **Context**: 2048 tokens
- **Language**: Primarily English

**Alternative Models** (Experimental):
```env
# Larger models (require more VRAM)
MODEL_NAME=google/gemma-2-7b  # ~14GB
MODEL_NAME=google/gemma-2-9b  # ~18GB

# Smaller models (less capable but faster)
MODEL_NAME=google/gemma-2-2b-it  # Instruction-tuned variant
```

**Model Selection Criteria**:
- **2B**: Best for learning and demonstration (recommended)
- **7B**: Better quality but requires 16GB+ VRAM
- **9B**: Highest quality but requires 24GB+ VRAM

### Device Configuration

**Automatic Selection** (Recommended):
```env
DEVICE=auto
```
- Automatically selects CUDA if available, falls back to CPU

**Manual Selection**:
```env
# Use first CUDA device
DEVICE=cuda:0

# Use specific CUDA device
DEVICE=cuda:1

# Force CPU usage
DEVICE=cpu

# Use MPS (Apple Silicon)
DEVICE=mps
```

**Device-Specific Settings**:

| Device | Recommended Settings |
|--------|---------------------|
| **RTX 4090** | `DEVICE=cuda:0`, `TORCH_DTYPE=float16` |
| **RTX 3080** | `DEVICE=cuda:0`, `TORCH_DTYPE=float16`, `MAX_LENGTH=1024` |
| **CPU (16+ cores)** | `DEVICE=cpu`, `TORCH_DTYPE=float32` |
| **Apple M1/M2** | `DEVICE=mps`, `TORCH_DTYPE=float16` |

### Memory Optimization

**For Limited VRAM** (<8GB):
```env
DEVICE=cpu
TORCH_DTYPE=float16
LOW_CPU_MEM_USAGE=true
MAX_LENGTH=1024
```

**For Abundant VRAM** (16GB+):
```env
DEVICE=cuda:0
TORCH_DTYPE=float16
MAX_LENGTH=2048
COMPILE_MODEL=true
```

**Quantization Options**:
```env
# 8-bit quantization (saves ~50% memory)
LOAD_IN_8BIT=true
TORCH_DTYPE=auto

# 4-bit quantization (saves ~75% memory)
LOAD_IN_4BIT=true
TORCH_DTYPE=auto
```

---

## Service Configuration

### Network Settings

**Local Development**:
```env
# LLM Service
HOST=127.0.0.1  # Local only
PORT=8001

# Main Application
LLM_SERVICE_URL=http://localhost:8001
```

**Network Access** (Multiple machines):
```env
# LLM Service
HOST=0.0.0.0  # Listen on all interfaces
PORT=8001

# Main Application
LLM_SERVICE_URL=http://192.168.1.100:8001  # Replace with server IP
```

**Docker Deployment**:
```env
# LLM Service
HOST=0.0.0.0
PORT=8001

# Main Application  
LLM_SERVICE_URL=http://llm-service:8001  # Docker service name
```

### CORS Configuration

**Development** (Permissive):
```env
ALLOWED_ORIGINS=*
```

**Production** (Restrictive):
```env
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

**Local with Specific Ports**:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,http://127.0.0.1:3000
```

### Logging Configuration

**Log Levels**:
```env
# Minimal logging
LOG_LEVEL=error

# Standard logging
LOG_LEVEL=info  

# Verbose logging
LOG_LEVEL=debug
```

**Log Destinations**:
```env
# Console only (default)
LOG_HANDLER=console

# File logging (future enhancement)
LOG_HANDLER=file
LOG_FILE=./logs/service.log
```

---

## Performance Tuning

### Hardware-Specific Optimizations

**NVIDIA RTX 4090**:
```env
# LLM Service
DEVICE=cuda:0
TORCH_DTYPE=float16
COMPILE_MODEL=true
USE_FLASH_ATTENTION=true
MAX_LENGTH=2048
BATCH_SIZE=1

# Expected Performance: 50-80 tokens/second
```

**NVIDIA RTX 3080**:
```env
# LLM Service
DEVICE=cuda:0
TORCH_DTYPE=float16
MAX_LENGTH=1024
LOAD_IN_8BIT=false
BATCH_SIZE=1

# Expected Performance: 30-50 tokens/second
```

**Apple M1/M2**:
```env
# LLM Service
DEVICE=mps
TORCH_DTYPE=float16
MAX_LENGTH=1024
LOW_CPU_MEM_USAGE=true

# Expected Performance: 15-25 tokens/second
```

**CPU-Only (16+ cores)**:
```env
# LLM Service
DEVICE=cpu
TORCH_DTYPE=float32
MAX_LENGTH=512
LOW_CPU_MEM_USAGE=true
WORKERS=1

# Expected Performance: 5-10 tokens/second
```

### Memory Management

**Conservative** (4GB VRAM):
```env
DEVICE=cuda:0
TORCH_DTYPE=float16
LOAD_IN_8BIT=true
MAX_LENGTH=512
LOW_CPU_MEM_USAGE=true
```

**Balanced** (8GB VRAM):
```env
DEVICE=cuda:0
TORCH_DTYPE=float16
MAX_LENGTH=1024
LOW_CPU_MEM_USAGE=true
```

**Aggressive** (16GB+ VRAM):
```env
DEVICE=cuda:0
TORCH_DTYPE=float16
MAX_LENGTH=2048
COMPILE_MODEL=true
```

### Network Optimization

**Local Development**:
```env
# Main Application
LLM_SERVICE_TIMEOUT=10  # Fast local network

# LLM Service
WORKERS=1  # Single worker for development
```

**Production Deployment**:
```env
# Main Application
LLM_SERVICE_TIMEOUT=30  # Account for network latency

# LLM Service
WORKERS=2  # Multiple workers for concurrency
```

---

## Security Settings

### Authentication

**No Authentication** (Development):
```env
# LLM Service
API_KEY=  # Empty or not set

# Main Application
LLM_SERVICE_API_KEY=  # Empty or not set
```

**API Key Authentication** (Production):
```env
# LLM Service
API_KEY=your-secure-random-key-here

# Main Application
LLM_SERVICE_API_KEY=your-secure-random-key-here
```

**Generate Secure API Key**:
```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -base64 32
```

### Network Security

**CORS Settings**:
```env
# Development (permissive)
ALLOWED_ORIGINS=*

# Staging
ALLOWED_ORIGINS=https://staging.your-domain.com

# Production (restrictive)
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

**Host Binding**:
```env
# Local only (most secure)
HOST=127.0.0.1

# Network access (less secure)
HOST=0.0.0.0
```

### Data Privacy

**Model Caching**:
```env
# Local caching (default)
MODEL_CACHE_DIR=./models
HF_HOME=./cache/huggingface

# System-wide caching
MODEL_CACHE_DIR=/opt/models
HF_HOME=/opt/cache/huggingface

# No persistent caching (most private)
MODEL_CACHE_DIR=/tmp/models
```

**Logging Privacy**:
```env
# Minimal logging (more private)
LOG_LEVEL=error

# No user input logging (future enhancement)
LOG_USER_INPUTS=false
```

---

## Development vs Production

### Development Configuration

**Main Application**:
```env
# token_visualizer/.env (Development)
LLM_SERVICE_URL=http://localhost:8001
LLM_SERVICE_TIMEOUT=10
DEBUG=true
RELOAD=true
REFLEX_LOG_LEVEL=debug
```

**LLM Service**:
```env
# llm_service/.env (Development)
MODEL_NAME=google/gemma-2-2b
DEVICE=auto
HOST=127.0.0.1
PORT=8001
LOG_LEVEL=debug
WORKERS=1
RELOAD=true
```

### Production Configuration

**Main Application**:
```env
# token_visualizer/.env (Production)
LLM_SERVICE_URL=http://llm-service:8001
LLM_SERVICE_TIMEOUT=30
LLM_SERVICE_API_KEY=your-secure-api-key
DEBUG=false
RELOAD=false
REFLEX_LOG_LEVEL=info
```

**LLM Service**:
```env
# llm_service/.env (Production)
MODEL_NAME=google/gemma-2-2b
DEVICE=cuda:0
HOST=0.0.0.0
PORT=8001
LOG_LEVEL=info
WORKERS=2
API_KEY=your-secure-api-key
ALLOWED_ORIGINS=https://your-domain.com
TORCH_DTYPE=float16
MAX_LENGTH=2048
```

### Container Configuration

**Docker Compose Example**:
```yaml
# docker-compose.yml
version: '3.8'

services:
  llm-service:
    build: ./llm_service
    environment:
      - MODEL_NAME=google/gemma-2-2b
      - DEVICE=cuda:0
      - HOST=0.0.0.0
      - PORT=8001
      - API_KEY=${LLM_API_KEY}
    volumes:
      - model_cache:/app/models
      - hf_cache:/app/cache
    ports:
      - "8001:8001"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  token-visualizer:
    build: ./token_visualizer
    environment:
      - LLM_SERVICE_URL=http://llm-service:8001
      - LLM_SERVICE_API_KEY=${LLM_API_KEY}
      - REFLEX_LOG_LEVEL=info
    ports:
      - "3000:3000"
      - "8000:8000"
    depends_on:
      - llm-service

volumes:
  model_cache:
  hf_cache:
```

### Environment File Templates

**Development Template**:
```bash
# Copy and customize for development
cp token_visualizer/.env.example token_visualizer/.env
cp llm_service/.env.example llm_service/.env

# Edit with your preferences
nano token_visualizer/.env
nano llm_service/.env
```

**Production Template**:
```bash
# Use secure values for production
cp production.env.template .env

# Set secure API keys
echo "LLM_API_KEY=$(openssl rand -base64 32)" >> .env

# Review all settings
nano .env
```

### Configuration Validation

**Startup Checks**:
The application performs validation on startup:

1. **Model Accessibility**: Verifies model can be downloaded/loaded
2. **Device Availability**: Checks CUDA/MPS availability if specified
3. **Network Connectivity**: Tests service-to-service communication
4. **Authentication**: Validates API keys if configured
5. **Resource Requirements**: Checks available memory and disk space

**Manual Validation**:
```bash
# Test LLM service configuration
cd llm_service
uv run python -c "
from config.settings import Settings
settings = Settings()
print(f'Model: {settings.model_name}')
print(f'Device: {settings.device}')
print(f'Valid config: {settings.validate()}')
"

# Test main application configuration
cd token_visualizer
uv run python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print(f'LLM Service URL: {os.getenv(\"LLM_SERVICE_URL\")}')
print(f'Timeout: {os.getenv(\"LLM_SERVICE_TIMEOUT\")}')
"
```

This configuration guide provides comprehensive coverage of all settings needed to run the Token Visualizer in various environments, from development to production deployment.
