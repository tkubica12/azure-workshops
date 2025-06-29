"""Configuration management for Token Visualizer application."""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv


@dataclass
class AzureOpenAIConfig:
    """Configuration for Azure OpenAI service."""
    endpoint: str
    deployment_name: str
    api_version: str
    api_key: Optional[str] = None
    use_azure_default_credentials: bool = True
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT is required")
        if not self.deployment_name:
            raise ValueError("AZURE_OPENAI_DEPLOYMENT_NAME is required")
        if not self.use_azure_default_credentials and not self.api_key:
            raise ValueError("Either AZURE_OPENAI_API_KEY must be set or USE_AZURE_DEFAULT_CREDENTIALS must be true")


@dataclass
class AppConfig:
    """Main application configuration."""
    azure_openai: AzureOpenAIConfig
    debug: bool = False
    
    @classmethod
    def load_from_env(cls) -> "AppConfig":
        """Load configuration from environment variables."""
        # Load .env file if it exists
        load_dotenv()
        
        # Get Azure OpenAI configuration
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        use_aad = os.getenv("USE_AZURE_DEFAULT_CREDENTIALS", "true").lower() == "true"
        
        # Create Azure OpenAI config
        azure_openai_config = AzureOpenAIConfig(
            endpoint=endpoint,
            deployment_name=deployment_name,
            api_version=api_version,
            api_key=api_key,
            use_azure_default_credentials=use_aad
        )
        
        # Get general app configuration
        debug = os.getenv("DEBUG", "false").lower() == "true"
        
        return cls(
            azure_openai=azure_openai_config,
            debug=debug
        )
    
    def is_valid(self) -> tuple[bool, str]:
        """Check if configuration is valid."""
        try:
            # This will raise ValueError if invalid
            self.azure_openai.__post_init__()
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
            "endpoint": config.azure_openai.endpoint,
            "deployment": config.azure_openai.deployment_name,
            "api_version": config.azure_openai.api_version,
            "auth_method": "Azure Default Credentials" if config.azure_openai.use_azure_default_credentials else "API Key",
            "has_api_key": bool(config.azure_openai.api_key),
            "debug": config.debug
        }
    except Exception as e:
        return {
            "valid": False,
            "message": f"Configuration error: {str(e)}",
            "error": str(e)
        }
