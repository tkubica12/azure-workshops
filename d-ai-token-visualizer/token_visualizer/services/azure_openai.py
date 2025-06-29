"""Azure OpenAI API client service for Token Visualizer application."""

import asyncio
import math
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from ..utils.config import get_config, AzureOpenAIConfig


@dataclass
class TokenProbability:
    """Represents a token with its probability information."""
    token: str
    logprob: float
    probability: float  # Converted from logprob (0-1 range)
    percentage: float   # Probability as percentage (0-100 range)


@dataclass
class TokenGenerationResult:
    """Result from token generation API call."""
    generated_text: str
    selected_token: TokenProbability
    top_alternatives: List[TokenProbability]
    raw_response: Any  # Store the full OpenAI response for debugging


class AzureOpenAIClient:
    """Azure OpenAI API client with authentication and error handling."""
    
    def __init__(self, config: Optional[AzureOpenAIConfig] = None):
        """Initialize the Azure OpenAI client.
        
        Args:
            config: Optional configuration. If None, loads from environment.
        """
        self.config = config or get_config().azure_openai
        self._client: Optional[AzureOpenAI] = None
        self._is_initialized = False
    
    def _initialize_client(self) -> AzureOpenAI:
        """Initialize the Azure OpenAI client with proper authentication."""
        if self._client is not None and self._is_initialized:
            return self._client
        
        try:
            if self.config.use_azure_default_credentials:
                # Use Azure Default Credentials (AAD)
                credential = DefaultAzureCredential()
                token_provider = get_bearer_token_provider(
                    credential,
                    "https://cognitiveservices.azure.com/.default"
                )
                
                self._client = AzureOpenAI(
                    azure_endpoint=self.config.endpoint,
                    azure_ad_token_provider=token_provider,
                    api_version=self.config.api_version
                )
            else:
                # Use API Key authentication
                if not self.config.api_key:
                    raise ValueError("API key is required when not using Azure Default Credentials")
                
                self._client = AzureOpenAI(
                    azure_endpoint=self.config.endpoint,
                    api_key=self.config.api_key,
                    api_version=self.config.api_version
                )
            
            self._is_initialized = True
            return self._client
            
        except Exception as e:
            raise ConnectionError(f"Failed to initialize Azure OpenAI client: {str(e)}")
    
    def test_connection(self) -> Tuple[bool, str]:
        """Test the API connection with a simple request.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            client = self._initialize_client()
            
            # Simple test request
            response = client.chat.completions.create(
                model=self.config.deployment_name,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=1,
                temperature=0.0
            )
            
            if response.choices and response.choices[0].message.content:
                return True, "Connection successful"
            else:
                return False, "No response content received"
                
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def _logprob_to_probability(self, logprob: float) -> float:
        """Convert log probability to probability (0-1 range)."""
        return math.exp(logprob)
    
    def _create_token_probability(self, token: str, logprob: float) -> TokenProbability:
        """Create a TokenProbability object from token and logprob."""
        probability = self._logprob_to_probability(logprob)
        percentage = probability * 100.0
        
        return TokenProbability(
            token=token,
            logprob=logprob,
            probability=probability,
            percentage=percentage
        )
    
    def generate_with_logprobs(
        self,
        prompt: str,
        max_tokens: int = 1,
        temperature: float = 0.7,
        top_logprobs: int = 5
    ) -> TokenGenerationResult:
        """Generate text with logprobs for token analysis.
        
        Args:
            prompt: Input prompt for generation
            max_tokens: Maximum tokens to generate (usually 1 for token-by-token)
            temperature: Sampling temperature (0.0 = deterministic, 1.0 = more random)
            top_logprobs: Number of top alternative tokens to return
            
        Returns:
            TokenGenerationResult with generated token and alternatives
            
        Raises:
            ConnectionError: If API connection fails
            ValueError: If the response format is unexpected
        """
        try:
            client = self._initialize_client()
            
            response = client.chat.completions.create(
                model=self.config.deployment_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
                logprobs=True,
                top_logprobs=top_logprobs
            )
            
            if not response.choices or not response.choices[0].message.content:
                raise ValueError("No content in API response")
            
            choice = response.choices[0]
            generated_text = choice.message.content
            
            # Extract logprobs data
            if not choice.logprobs or not choice.logprobs.content:
                raise ValueError("No logprobs data in API response")
            
            # Get the first (and usually only) token's logprobs
            first_token_data = choice.logprobs.content[0]
            
            # Create selected token probability
            selected_token = self._create_token_probability(
                first_token_data.token,
                first_token_data.logprob
            )
            
            # Create alternative token probabilities
            top_alternatives = []
            if first_token_data.top_logprobs:
                for alt_token_data in first_token_data.top_logprobs:
                    alt_token_prob = self._create_token_probability(
                        alt_token_data.token,
                        alt_token_data.logprob
                    )
                    top_alternatives.append(alt_token_prob)
            
            return TokenGenerationResult(
                generated_text=generated_text,
                selected_token=selected_token,
                top_alternatives=top_alternatives,
                raw_response=response
            )
            
        except Exception as e:
            if isinstance(e, (ConnectionError, ValueError)):
                raise
            else:
                raise ConnectionError(f"API call failed: {str(e)}")
    
    def generate_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 100,
        temperature: float = 0.7
    ) -> str:
        """Generate a standard completion without logprobs.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text content
            
        Raises:
            ConnectionError: If API connection fails
        """
        try:
            client = self._initialize_client()
            
            response = client.chat.completions.create(
                model=self.config.deployment_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            if not response.choices or not response.choices[0].message.content:
                raise ValueError("No content in API response")
            
            return response.choices[0].message.content
            
        except Exception as e:
            if isinstance(e, (ConnectionError, ValueError)):
                raise
            else:
                raise ConnectionError(f"API call failed: {str(e)}")


# Global client instance for the application
_client: Optional[AzureOpenAIClient] = None


def get_azure_openai_client() -> AzureOpenAIClient:
    """Get the global Azure OpenAI client instance."""
    global _client
    if _client is None:
        _client = AzureOpenAIClient()
    return _client


def test_azure_openai_service() -> Dict[str, Any]:
    """Test the Azure OpenAI service and return status information.
    
    Returns:
        Dict with test results and service information
    """
    try:
        client = get_azure_openai_client()
        
        # Test basic connection
        connection_success, connection_message = client.test_connection()
        
        if not connection_success:
            return {
                "success": False,
                "message": connection_message,
                "connection_test": False,
                "logprobs_test": False
            }
        
        # Test logprobs functionality
        try:
            result = client.generate_with_logprobs(
                prompt="The capital of France is",
                max_tokens=1,
                temperature=0.0,
                top_logprobs=3
            )
            
            return {
                "success": True,
                "message": "Azure OpenAI service is working correctly",
                "connection_test": True,
                "logprobs_test": True,
                "test_result": {
                    "prompt": "The capital of France is",
                    "generated_text": result.generated_text,
                    "selected_token": {
                        "token": result.selected_token.token,
                        "probability": f"{result.selected_token.percentage:.2f}%"
                    },
                    "alternatives_count": len(result.top_alternatives),
                    "top_alternatives": [
                        {
                            "token": alt.token,
                            "probability": f"{alt.percentage:.2f}%"
                        }
                        for alt in result.top_alternatives[:3]
                    ]
                }
            }
            
        except Exception as logprobs_error:
            return {
                "success": False,
                "message": f"Logprobs test failed: {str(logprobs_error)}",
                "connection_test": True,
                "logprobs_test": False,
                "logprobs_error": str(logprobs_error)
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Service test failed: {str(e)}",
            "connection_test": False,
            "logprobs_test": False,
            "error": str(e)
        }
