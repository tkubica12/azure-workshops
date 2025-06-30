"""Configuration management for Token Visualizer application."""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv


@dataclass
class LocalLLMConfig:
    """Configuration for Local LLM service."""
    model_name: str
    hf_token: str
    device: str = "auto"
    use_quantization: bool = True
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.model_name:
            raise ValueError("LOCAL_MODEL_NAME is required")
        if not self.hf_token or self.hf_token == "your_hf_token_here":
            raise ValueError("HUGGINGFACE_TOKEN is required - get it from https://huggingface.co/settings/tokens")


# Legacy Azure OpenAI Config (kept for backwards compatibility)
@dataclass
class AzureOpenAIConfig:
    """Configuration for Azure OpenAI service (deprecated)."""
    endpoint: str = ""
    deployment_name: str = ""
    api_version: str = ""
    api_key: Optional[str] = None
    use_azure_default_credentials: bool = True


@dataclass
class AppConfig:
    """Main application configuration."""
    local_llm: LocalLLMConfig
    debug: bool = False
    
    @classmethod
    def load_from_env(cls) -> "AppConfig":
        """Load configuration from environment variables."""
        # Load .env file if it exists
        load_dotenv()
        
        # Get Local LLM configuration
        model_name = os.getenv("LOCAL_MODEL_NAME", "google/gemma-2-2b")
        hf_token = os.getenv("HUGGINGFACE_TOKEN", "")
        device = os.getenv("DEVICE", "auto")
        use_quantization = os.getenv("USE_QUANTIZATION", "true").lower() == "true"
        
        # Create Local LLM config
        local_llm_config = LocalLLMConfig(
            model_name=model_name,
            hf_token=hf_token,
            device=device,
            use_quantization=use_quantization
        )
        
        # Get general app configuration
        debug = os.getenv("DEBUG", "false").lower() == "true"
        
        return cls(
            local_llm=local_llm_config,
            debug=debug
        )
    
    def is_valid(self) -> tuple[bool, str]:
        """Check if configuration is valid."""
        try:
            # This will raise ValueError if invalid
            self.local_llm.__post_init__()
            return True, "Configuration is valid"
        except ValueError as e:
            return False, str(e)


# Global configuration instance
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = AppConfig.load_from_env()
    return _config


def reload_config() -> AppConfig:
    """Reload configuration from environment variables."""
    global _config
    _config = AppConfig.load_from_env()
    return _config


def test_config() -> dict:
    """Test configuration and return status information."""
    try:
        config = get_config()
        is_valid, message = config.is_valid()
        
        return {
            "valid": is_valid,
            "message": message,
            "model_name": config.local_llm.model_name,
            "device": config.local_llm.device,
            "use_quantization": config.local_llm.use_quantization,
            "has_hf_token": bool(config.local_llm.hf_token and config.local_llm.hf_token != "your_hf_token_here"),
            "debug": config.debug
        }
    except Exception as e:
        return {
            "valid": False,
            "message": f"Configuration error: {str(e)}",
            "error": str(e)
        }
