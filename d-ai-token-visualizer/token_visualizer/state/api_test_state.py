"""State management for API testing functionality."""

import reflex as rx
from typing import Dict, Any, Optional, List
from ..services.azure_openai import get_azure_openai_client, TokenGenerationResult


class APITestState(rx.State):
    """State for managing API testing functionality."""
    
    # Form inputs
    test_prompt: str = "The capital of France is"
    max_tokens: int = 1
    temperature: float = 0.7
    top_logprobs: int = 5
    
    # Test results - store individual fields for easier UI access
    is_testing: bool = False
    test_result: Optional[Dict[str, Any]] = None
    test_error: str = ""
    has_test_result: bool = False
    
    # Individual result fields for easier UI binding
    result_prompt: str = ""
    result_generated_text: str = ""
    result_selected_token: str = ""
    result_selected_probability: str = ""
    result_alternatives: List[Dict[str, str]] = []
    result_raw_response: str = ""
    
    def set_test_prompt(self, prompt: str):
        """Set the test prompt."""
        self.test_prompt = prompt
    
    def set_max_tokens(self, tokens: str):
        """Set max tokens from string input."""
        try:
            self.max_tokens = max(1, min(10, int(tokens)))
        except ValueError:
            self.max_tokens = 1
    
    def set_temperature(self, temp: str):
        """Set temperature from string input."""
        try:
            self.temperature = max(0.0, min(2.0, float(temp)))
        except ValueError:
            self.temperature = 0.7
    
    def set_top_logprobs(self, logprobs: str):
        """Set top logprobs from string input."""
        try:
            self.top_logprobs = max(1, min(20, int(logprobs)))
        except ValueError:
            self.top_logprobs = 5
    
    async def run_custom_test(self):
        """Run a custom test with the current form values."""
        self.is_testing = True
        self.test_error = ""
        self.test_result = None
        self.has_test_result = False
        
        # Clear previous results
        self.result_prompt = ""
        self.result_generated_text = ""
        self.result_selected_token = ""
        self.result_selected_probability = ""
        self.result_alternatives = []
        self.result_raw_response = ""
        
        try:
            client = get_azure_openai_client()
            
            # Run the test
            result = client.generate_with_logprobs(
                prompt=self.test_prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_logprobs=self.top_logprobs
            )
            
            # Store individual fields for UI binding
            self.result_prompt = self.test_prompt
            self.result_generated_text = result.generated_text
            self.result_selected_token = result.selected_token.token
            self.result_selected_probability = f"{result.selected_token.percentage:.2f}%"
            
            # Store alternatives as list of dicts
            self.result_alternatives = [
                {
                    "token": alt.token,
                    "probability": f"{alt.percentage:.2f}%",
                    "logprob": f"{alt.logprob:.4f}"
                }
                for alt in result.top_alternatives
            ]
            
            # Store raw response (truncated for UI)
            self.result_raw_response = f"Generated: '{result.generated_text}' | Selected: '{result.selected_token.token}' ({result.selected_token.percentage:.2f}%) | Alternatives: {len(result.top_alternatives)} tokens"
            
            # Convert result to dict for backward compatibility
            self.test_result = {
                "prompt": self.test_prompt,
                "generated_text": result.generated_text,
                "selected_token": {
                    "token": result.selected_token.token,
                    "logprob": result.selected_token.logprob,
                    "probability": result.selected_token.probability,
                    "percentage": result.selected_token.percentage
                },
                "top_alternatives": [
                    {
                        "token": alt.token,
                        "logprob": alt.logprob,
                        "probability": alt.probability,
                        "percentage": alt.percentage
                    }
                    for alt in result.top_alternatives
                ],
                "parameters": {
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature,
                    "top_logprobs": self.top_logprobs
                }
            }
            
            self.has_test_result = True
            
        except Exception as e:
            self.test_error = str(e)
            self.test_result = None
            self.has_test_result = False
        
        finally:
            self.is_testing = False
    
    def clear_test_results(self):
        """Clear test results and errors."""
        self.test_result = None
        self.test_error = ""
        self.has_test_result = False
        self.is_testing = False
        
        # Clear individual result fields
        self.result_prompt = ""
        self.result_generated_text = ""
        self.result_selected_token = ""
        self.result_selected_probability = ""
        self.result_alternatives = []
        self.result_raw_response = ""
    
    def use_preset_prompt(self, preset: str):
        """Set a preset prompt for testing."""
        presets = {
            "simple": "The capital of France is",
            "story": "Once upon a time, in a land far away, there was a",
            "technical": "The main difference between Python and JavaScript is",
            "creative": "The most beautiful thing about nature is",
            "question": "What is the meaning of"
        }
        
        if preset in presets:
            self.test_prompt = presets[preset]
