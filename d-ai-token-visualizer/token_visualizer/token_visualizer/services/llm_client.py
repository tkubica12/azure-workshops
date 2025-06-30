"""HTTP client for the Local LLM service."""
import httpx
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

from ..utils.config import get_config, LLMServiceConfig


@dataclass
class TokenProbability:
    """Token with its probability."""
    token: str
    probability: float
    logprob: float
    
    def probability_percentage(self) -> str:
        """Return probability as percentage string."""
        return f"{self.probability * 100:.1f}%"


@dataclass 
class TokenGenerationResult:
    """Result from token generation with probabilities."""
    prompt: str
    generated_text: str
    selected_token: str
    selected_probability: float
    alternatives: List[TokenProbability]
    raw_response: Dict[str, Any]


class LLMServiceClient:
    """HTTP client for the Local LLM service with retry logic and health monitoring."""
    
    def __init__(self, config: Optional[LLMServiceConfig] = None):
        """Initialize the LLM service client."""
        self.config = config or get_config().llm_service
        self.base_url = self.config.service_url.rstrip('/')
        
        # HTTP client configuration
        self.timeout = httpx.Timeout(30.0, connect=5.0)
        self.retry_attempts = 3
        self.retry_delay = 1.0  # seconds
        
        # Health monitoring
        self._last_health_check: Optional[datetime] = None
        self._health_check_interval = timedelta(minutes=5)
        self._is_healthy = False
        
        # Create HTTP client
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={"Content-Type": "application/json"}
        )
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.client.aclose()
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        """Make HTTP request with retry logic."""
        last_exception = None
        
        for attempt in range(self.retry_attempts):
            try:
                response = await self.client.request(method, endpoint, **kwargs)
                return response
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                last_exception = e
                if attempt < self.retry_attempts - 1:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                continue
            except Exception as e:
                # Don't retry other exceptions
                raise e
        
        # All retries failed
        raise last_exception
    
    async def health_check(self) -> Tuple[bool, str]:
        """Check if the LLM service is healthy and responding."""
        try:
            response = await self._make_request("GET", "/health")
            
            if response.status_code == 200:
                data = response.json()
                self._is_healthy = True
                self._last_health_check = datetime.now()
                return True, data.get("message", "Service is healthy")
            else:
                self._is_healthy = False
                return False, f"Service returned status {response.status_code}"
                
        except Exception as e:
            self._is_healthy = False
            return False, f"Health check failed: {str(e)}"
    
    async def get_service_status(self) -> Tuple[bool, Dict[str, Any]]:
        """Get detailed service status and model information."""
        try:
            response = await self._make_request("GET", "/api/v1/status")
            
            if response.status_code == 200:
                data = response.json()
                return True, data
            else:
                return False, {"error": f"Status endpoint returned {response.status_code}"}
                
        except Exception as e:
            return False, {"error": f"Status check failed: {str(e)}"}
    
    def _should_check_health(self) -> bool:
        """Check if we should perform a health check."""
        if self._last_health_check is None:
            return True
        return datetime.now() - self._last_health_check > self._health_check_interval
    
    async def generate_tokens_with_probabilities(
        self,
        prompt: str,
        max_tokens: int = 1,
        temperature: float = 0.7,
        top_logprobs: int = 5
    ) -> TokenGenerationResult:
        """Generate tokens with probabilities from the LLM service."""
        # Check health if needed
        if self._should_check_health():
            await self.health_check()
        
        if not self._is_healthy:
            raise RuntimeError("LLM service is not healthy. Check service status.")
        
        # Prepare request payload
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_logprobs": top_logprobs
        }
        
        try:
            response = await self._make_request("POST", "/api/v1/generate", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_generation_response(data)
            else:
                error_msg = f"Generation failed with status {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f": {error_data.get('detail', 'Unknown error')}"
                except:
                    error_msg += f": {response.text}"
                raise RuntimeError(error_msg)
                
        except Exception as e:
            if isinstance(e, RuntimeError):
                raise e
            raise RuntimeError(f"Token generation failed: {str(e)}")
    
    def _parse_generation_response(self, data: Dict[str, Any]) -> TokenGenerationResult:
        """Parse the response from the LLM service into our result format."""
        try:
            # Extract main fields
            prompt = data["prompt"]
            generated_text = data["generated_text"]
            
            # Get selected token info
            selected_token_data = data["selected_token"]
            selected_token = selected_token_data["token"]
            selected_probability = selected_token_data["probability"]
            
            # Parse token alternatives
            alternatives = []
            for alt in data["top_alternatives"]:
                alternatives.append(TokenProbability(
                    token=alt["token"],
                    probability=alt["probability"],
                    logprob=alt["logprob"]
                ))
            
            return TokenGenerationResult(
                prompt=prompt,
                generated_text=generated_text,
                selected_token=selected_token,
                selected_probability=selected_probability,
                alternatives=alternatives,
                raw_response=data
            )
            
        except KeyError as e:
            raise ValueError(f"Invalid response format from LLM service: missing field {e}")
        except Exception as e:
            raise ValueError(f"Failed to parse LLM service response: {str(e)}")


# Global client instance for the application
_client: Optional[LLMServiceClient] = None


async def get_llm_client() -> LLMServiceClient:
    """Get the global LLM service client instance."""
    global _client
    if _client is None:
        _client = LLMServiceClient()
    return _client


async def close_llm_client():
    """Close the global LLM service client."""
    global _client
    if _client:
        await _client.close()
        _client = None


async def test_llm_service() -> Dict[str, Any]:
    """Test the LLM service connection and functionality."""
    result = {
        "timestamp": datetime.now().isoformat(),
        "service_url": get_config().llm_service.service_url,
        "health_check": {"success": False, "message": ""},
        "status_check": {"success": False, "data": {}},
        "generation_test": {"success": False, "result": None, "error": ""}
    }
    
    client = None
    try:
        client = LLMServiceClient()
        
        # Test health check
        health_success, health_message = await client.health_check()
        result["health_check"] = {
            "success": health_success,
            "message": health_message
        }
        
        if health_success:
            # Test status endpoint
            status_success, status_data = await client.get_service_status()
            result["status_check"] = {
                "success": status_success,
                "data": status_data
            }
            
            # Test generation if health and status are good
            if status_success:
                try:
                    generation_result = await client.generate_tokens_with_probabilities(
                        prompt="The capital of France is",
                        max_tokens=1,
                        temperature=0.7,
                        top_logprobs=5
                    )
                    
                    result["generation_test"] = {
                        "success": True,
                        "result": {
                            "prompt": generation_result.prompt,
                            "generated_text": generation_result.generated_text,
                            "selected_token": generation_result.selected_token,
                            "selected_probability": f"{generation_result.selected_probability:.3f}",
                            "alternatives_count": len(generation_result.alternatives),
                            "alternatives": [
                                {
                                    "token": alt.token,
                                    "probability": f"{alt.probability:.3f}",
                                    "percentage": alt.probability_percentage()
                                }
                                for alt in generation_result.alternatives[:3]  # Show top 3
                            ]
                        },
                        "error": ""
                    }
                except Exception as e:
                    result["generation_test"] = {
                        "success": False,
                        "result": None,
                        "error": str(e)
                    }
    
    except Exception as e:
        result["health_check"]["message"] = f"Failed to connect to service: {str(e)}"
    
    finally:
        if client:
            await client.close()
    
    return result
