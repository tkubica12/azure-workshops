"""Configuration settings for the Local LLM Service."""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMServiceSettings(BaseSettings):
    """Configuration settings for the LLM service."""
    
    # Service configuration
    host: str = Field(default="0.0.0.0", description="Host to bind the service to")
    port: int = Field(default=8001, description="Port to bind the service to")
    reload: bool = Field(default=False, description="Enable auto-reload for development")
    log_level: str = Field(default="info", description="Logging level")
    
    # Model configuration - map to environment variable names
    model_name: str = Field(default="google/gemma-2-2b", description="Hugging Face model name", alias="LOCAL_MODEL_NAME")
    device: str = Field(default="auto", description="Device for inference: auto, cuda, cpu", alias="DEVICE")
    use_quantization: bool = Field(default=True, description="Enable 4-bit quantization", alias="USE_QUANTIZATION")
    
    # Hugging Face configuration
    hf_token: Optional[str] = Field(default=None, description="Hugging Face authentication token", alias="HUGGINGFACE_TOKEN")
    
    # Generation parameters
    default_temperature: float = Field(default=0.7, description="Default sampling temperature")
    default_top_k: int = Field(default=5, description="Default number of top alternatives")
    default_max_new_tokens: int = Field(default=1, description="Default max tokens to generate")
    
    # Service limits
    max_prompt_length: int = Field(default=2048, description="Maximum prompt length in characters")
    request_timeout: int = Field(default=30, description="Request timeout in seconds")
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }


# Global settings instance
settings = LLMServiceSettings()
