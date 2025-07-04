# API Documentation

## LLM Service REST API

### Base URL
```
http://localhost:8001
```

### Authentication
If API key authentication is enabled, include the API key in the Authorization header:
```http
Authorization: Bearer YOUR_API_KEY
```

---

## Endpoints

### Health Check

#### GET /health
**Description**: Check if the service is running and healthy.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-01T12:00:00Z"
}
```

**Status Codes**:
- `200 OK`: Service is healthy
- `503 Service Unavailable`: Service is starting or model not loaded

---

### Service Status

#### GET /status
**Description**: Get detailed information about the service and model.

**Response**:
```json
{
  "service": {
    "status": "running",
    "version": "0.1.0",
    "uptime_seconds": 3600,
    "memory_usage_mb": 8192
  },
  "model": {
    "name": "google/gemma-2-2b",
    "loaded": true,
    "device": "cuda:0",
    "precision": "float16",
    "max_length": 2048,
    "vocab_size": 256000
  },
  "system": {
    "gpu_available": true,
    "gpu_name": "NVIDIA RTX 4090",
    "gpu_memory_total_mb": 24576,
    "gpu_memory_used_mb": 8192,
    "cpu_cores": 16,
    "system_memory_gb": 32
  }
}
```

**Status Codes**:
- `200 OK`: Status retrieved successfully
- `503 Service Unavailable`: Service is starting

---

### Token Generation

#### POST /generate
**Description**: Generate token probabilities for next token prediction.

**Request Body**:
```json
{
  "prompt": "The capital of France is",
  "temperature": 1.0,
  "max_tokens": 1,
  "top_k": 5
}
```

**Request Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Input text prompt |
| `temperature` | float | No | 1.0 | Sampling temperature (0.0-2.0) |
| `max_tokens` | integer | No | 1 | Maximum tokens to generate (1-100) |
| `top_k` | integer | No | 5 | Number of top tokens to return (1-50) |

**Response**:
```json
{
  "generated_text": " Paris",
  "tokens": [
    {
      "token": " Paris",
      "probability": 0.8234,
      "percentage": 82.34,
      "logprob": -0.1941,
      "rank": 1
    },
    {
      "token": " Lyon",
      "probability": 0.0892,
      "percentage": 8.92,
      "logprob": -2.4159,
      "rank": 2
    },
    {
      "token": " Marseille",
      "probability": 0.0567,
      "percentage": 5.67,
      "logprob": -2.8693,
      "rank": 3
    },
    {
      "token": " Nice",
      "probability": 0.0234,
      "percentage": 2.34,
      "logprob": -3.7492,
      "rank": 4
    },
    {
      "token": " Bordeaux",
      "probability": 0.0073,
      "percentage": 0.73,
      "logprob": -4.9164,
      "rank": 5
    }
  ],
  "metadata": {
    "model_name": "google/gemma-2-2b",
    "prompt_length": 23,
    "prompt_tokens": 6,
    "generation_time_ms": 156,
    "temperature_used": 1.0,
    "device": "cuda:0"
  }
}
```

**Error Responses**:

```json
// 400 Bad Request - Empty prompt
{
  "detail": "Prompt cannot be empty",
  "error_code": "EMPTY_PROMPT"
}

// 400 Bad Request - Prompt too long
{
  "detail": "Prompt exceeds maximum length of 2048 tokens",
  "error_code": "PROMPT_TOO_LONG"
}

// 422 Unprocessable Entity - Validation error
{
  "detail": [
    {
      "loc": ["body", "temperature"],
      "msg": "ensure this value is less than or equal to 2.0",
      "type": "value_error.number.not_le"
    }
  ]
}

// 503 Service Unavailable - Model not loaded
{
  "detail": "Model is not loaded. Please wait for model loading to complete.",
  "error_code": "MODEL_NOT_LOADED"
}

// 500 Internal Server Error - Generation failed
{
  "detail": "Token generation failed due to internal error",
  "error_code": "GENERATION_FAILED"
}
```

**Status Codes**:
- `200 OK`: Generation successful
- `400 Bad Request`: Invalid request parameters
- `422 Unprocessable Entity`: Validation error
- `503 Service Unavailable`: Model not loaded
- `500 Internal Server Error`: Generation failed

---

## Data Models

### TokenProbability
```python
class TokenProbability(BaseModel):
    token: str = Field(..., description="The token text")
    probability: float = Field(..., ge=0.0, le=1.0, description="Probability value (0.0-1.0)")
    percentage: float = Field(..., ge=0.0, le=100.0, description="Percentage value (0.0-100.0)")
    logprob: float = Field(..., description="Log probability value")
    rank: int = Field(..., ge=1, description="Rank among all possible tokens")
```

### GenerateRequest
```python
class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Input text prompt")
    temperature: float = Field(1.0, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: int = Field(1, ge=1, le=100, description="Maximum tokens to generate")
    top_k: int = Field(5, ge=1, le=50, description="Number of top tokens to return")
```

### GenerateResponse
```python
class GenerateResponse(BaseModel):
    generated_text: str = Field(..., description="Generated text")
    tokens: List[TokenProbability] = Field(..., description="Top-k token probabilities")
    metadata: Dict[str, Any] = Field(..., description="Generation metadata")
```

---

## Client Examples

### Python (httpx)
```python
import asyncio
import httpx

async def generate_tokens(prompt: str, temperature: float = 1.0):
    """Generate token probabilities using the LLM service."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/generate",
            json={
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": 1,
                "top_k": 5
            },
            headers={"Authorization": "Bearer YOUR_API_KEY"}  # If auth enabled
        )
        response.raise_for_status()
        return response.json()

# Usage
async def main():
    result = await generate_tokens("The capital of France is")
    
    print(f"Generated: {result['generated_text']}")
    print("Top alternatives:")
    for token in result['tokens']:
        print(f"  {token['token']}: {token['percentage']:.1f}%")

asyncio.run(main())
```

### JavaScript (fetch)
```javascript
async function generateTokens(prompt, temperature = 1.0) {
    const response = await fetch('http://localhost:8001/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer YOUR_API_KEY'  // If auth enabled
        },
        body: JSON.stringify({
            prompt: prompt,
            temperature: temperature,
            max_tokens: 1,
            top_k: 5
        })
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

// Usage
generateTokens("The capital of France is")
    .then(result => {
        console.log(`Generated: ${result.generated_text}`);
        console.log("Top alternatives:");
        result.tokens.forEach(token => {
            console.log(`  ${token.token}: ${token.percentage.toFixed(1)}%`);
        });
    })
    .catch(error => console.error('Error:', error));
```

### cURL Examples
```bash
# Basic generation
curl -X POST "http://localhost:8001/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "The capital of France is",
       "temperature": 1.0,
       "max_tokens": 1,
       "top_k": 5
     }'

# With authentication
curl -X POST "http://localhost:8001/generate" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -d '{
       "prompt": "The weather today is",
       "temperature": 0.8,
       "max_tokens": 1,
       "top_k": 10
     }'

# Health check
curl -X GET "http://localhost:8001/health"

# Status check
curl -X GET "http://localhost:8001/status"
```

---

## Rate Limiting

Currently, the API does not implement rate limiting. For production use, consider:

1. **Nginx rate limiting**: Limit requests per IP
2. **Application-level limiting**: Implement per-user quotas
3. **Queue management**: Handle concurrent requests gracefully

---

## Error Handling

### Error Response Format
All errors follow the FastAPI standard format:
```json
{
  "detail": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE"
}
```

### Common Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `EMPTY_PROMPT` | Prompt is empty or whitespace only | Provide non-empty prompt |
| `PROMPT_TOO_LONG` | Prompt exceeds maximum token length | Shorten the prompt |
| `MODEL_NOT_LOADED` | Model is still loading | Wait and retry |
| `GENERATION_FAILED` | Internal generation error | Check service logs |
| `INVALID_TEMPERATURE` | Temperature outside valid range | Use 0.0-2.0 range |
| `INVALID_MAX_TOKENS` | max_tokens outside valid range | Use 1-100 range |
| `INVALID_TOP_K` | top_k outside valid range | Use 1-50 range |

### Retry Logic
Implement exponential backoff for transient errors:
```python
async def generate_with_retry(prompt: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            return await generate_tokens(prompt)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 503:  # Service unavailable
                wait_time = 2 ** attempt  # Exponential backoff
                await asyncio.sleep(wait_time)
                continue
            raise
    raise Exception("Max retries exceeded")
```

---

## OpenAPI Documentation

The LLM service automatically generates OpenAPI documentation available at:
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **OpenAPI JSON**: http://localhost:8001/openapi.json

This interactive documentation allows you to:
- Test API endpoints directly
- View request/response schemas
- Download API specifications
- Generate client code
