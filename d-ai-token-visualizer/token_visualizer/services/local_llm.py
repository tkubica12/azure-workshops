"""Local LLM service for Token Visualizer application using Gemma 2 2B model."""

import os
import math
import time
import warnings
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from dotenv import load_dotenv

from ..utils.config import get_config, LocalLLMConfig


@dataclass
class TokenProbability:
    """Represents a token with its probability information."""
    token: str
    logprob: float
    probability: float  # Converted from logprob (0-1 range)
    percentage: float   # Probability as percentage (0-100 range)


@dataclass
class TokenGenerationResult:
    """Result from token generation."""
    generated_text: str
    selected_token: TokenProbability
    top_alternatives: List[TokenProbability]
    raw_logits: Any  # Store the raw logits for debugging
    generation_time: float  # Time taken for generation


class LocalLLMClient:
    """Local LLM client using Gemma 2 2B model with quantization support."""
    
    def __init__(self, config: Optional[LocalLLMConfig] = None):
        """Initialize the Local LLM client.
        
        Args:
            config: Optional configuration. If None, loads from environment.
        """
        self.config = config or get_config().local_llm
        self.tokenizer: Optional[AutoTokenizer] = None
        self.model: Optional[AutoModelForCausalLM] = None
        self.device: Optional[str] = None
        self._is_initialized = False
        
        # Suppress some warnings for cleaner output
        warnings.filterwarnings("ignore", category=UserWarning)
    
    def _detect_device(self) -> str:
        """Detect the best available device for inference."""
        if self.config.device == "auto":
            if torch.cuda.is_available():
                device = "cuda"
                print(f"🚀 Using CUDA: {torch.cuda.get_device_name(0)}")
                memory_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
                print(f"💾 GPU memory: {memory_gb:.1f} GB")
            else:
                device = "cpu"
                print("⚠️  CUDA not available, using CPU")
        else:
            device = self.config.device
        
        return device
    
    def _setup_quantization_config(self) -> Optional[BitsAndBytesConfig]:
        """Set up quantization configuration if enabled."""
        if not self.config.use_quantization:
            return None
        
        try:
            import bitsandbytes
            print(f"⚡ Using 4-bit quantization for memory efficiency")
            
            return BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4"
            )
        except ImportError:
            print("⚠️  BitsAndBytes not available - quantization disabled")
            return None
    
    def _initialize_model(self) -> Tuple[bool, str]:
        """Initialize the tokenizer and model.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        if self._is_initialized:
            return True, "Model already initialized"
        
        try:
            print(f"🔄 Loading tokenizer: {self.config.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config.model_name,
                token=self.config.hf_token
            )
            
            print(f"🔄 Loading model: {self.config.model_name}")
            self.device = self._detect_device()
            
            start_time = time.time()
            quantization_config = self._setup_quantization_config()
            
            # Load model with or without quantization
            if quantization_config is not None:
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.config.model_name,
                    quantization_config=quantization_config,
                    device_map="auto",
                    low_cpu_mem_usage=True,
                    token=self.config.hf_token
                )
            else:
                # Fallback to standard loading
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.config.model_name,
                    device_map="auto" if self.device == "cuda" else None,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    low_cpu_mem_usage=True,
                    token=self.config.hf_token
                )
                
                if self.device == "cpu":
                    self.model = self.model.to(self.device)
            
            load_time = time.time() - start_time
            
            # Get model info
            total_params = sum(p.numel() for p in self.model.parameters())
            params_billions = total_params / 1e9
            
            print(f"✅ Model loaded successfully in {load_time:.2f} seconds")
            print(f"📊 Model parameters: {params_billions:.2f}B")
            if quantization_config:
                print(f"💾 Memory efficient: 4-bit quantization (~75% memory reduction)")
            
            self._is_initialized = True
            return True, f"Model initialized successfully ({params_billions:.2f}B parameters)"
            
        except Exception as e:
            error_msg = f"Failed to initialize model: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def test_connection(self) -> Tuple[bool, str]:
        """Test the model loading and basic inference.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        # First ensure model is initialized
        success, message = self._initialize_model()
        if not success:
            return False, message
        
        try:
            # Simple test inference
            test_prompt = "The capital of France is"
            inputs = self.tokenizer(test_prompt, return_tensors="pt")
            
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=1,
                    do_sample=False,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            new_token = generated_text[len(test_prompt):]
            
            return True, f"Test successful - generated: '{new_token.strip()}'"
            
        except Exception as e:
            error_msg = f"Test failed: {str(e)}"
            return False, error_msg
    
    def _logprob_to_probability(self, logprob: float) -> float:
        """Convert log probability to probability."""
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
        """Generate text with probability information for next token.
        
        Args:
            prompt: Input text prompt
            max_tokens: Number of tokens to generate (typically 1 for interactive mode)
            temperature: Sampling temperature (0.0 = greedy, higher = more random)
            top_logprobs: Number of top alternative tokens to return
            
        Returns:
            TokenGenerationResult with generated text and probabilities
        """
        # Ensure model is initialized
        if not self._is_initialized:
            success, message = self._initialize_model()
            if not success:
                raise RuntimeError(f"Model initialization failed: {message}")
        
        try:
            generation_start = time.time()
            
            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt")
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Get logits for the next token (before sampling)
            with torch.no_grad():
                model_outputs = self.model(**inputs)
                logits = model_outputs.logits[0, -1, :]  # Last token logits
                
                # Convert logits to log probabilities
                log_probs = F.log_softmax(logits, dim=-1)
                
                # Get top-k alternatives
                top_logprobs_tensor, top_indices = torch.topk(log_probs, top_logprobs)
                
                # Create alternative tokens list
                top_alternatives = []
                for logprob, token_id in zip(top_logprobs_tensor, top_indices):
                    token = self.tokenizer.decode([token_id.item()])
                    token_prob = self._create_token_probability(token, logprob.item())
                    top_alternatives.append(token_prob)
            
            # Generate one token using sampling
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    do_sample=True if temperature > 0 else False,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Extract the generated text and token
            generated_sequence = outputs[0]
            full_generated_text = self.tokenizer.decode(generated_sequence, skip_special_tokens=True)
            
            # Get the actually selected token
            new_token_id = generated_sequence[-1].item()
            new_token = self.tokenizer.decode([new_token_id])
            
            # Get the probability of the selected token
            selected_logprob = log_probs[new_token_id].item()
            selected_token = self._create_token_probability(new_token, selected_logprob)
            
            generation_end = time.time()
            generation_time = generation_end - generation_start
            
            return TokenGenerationResult(
                generated_text=full_generated_text,
                selected_token=selected_token,
                top_alternatives=top_alternatives,
                raw_logits=logits.cpu().numpy() if hasattr(logits, 'cpu') else logits,
                generation_time=generation_time
            )
            
        except Exception as e:
            raise RuntimeError(f"Generation failed: {str(e)}")


# Global client instance for the application
_client: Optional[LocalLLMClient] = None


def get_local_llm_client() -> LocalLLMClient:
    """Get the global Local LLM client instance."""
    global _client
    if _client is None:
        _client = LocalLLMClient()
    return _client


def test_local_llm_service() -> Dict[str, Any]:
    """Test the Local LLM service and return status information."""
    try:
        client = get_local_llm_client()
        success, message = client.test_connection()
        
        if success:
            # Test a simple generation
            result = client.generate_with_logprobs(
                prompt="The capital of Slovakia is",
                max_tokens=1,
                temperature=0.7,
                top_logprobs=5
            )
            
            return {
                "status": "success",
                "message": message,
                "model_name": client.config.model_name,
                "device": client.device,
                "quantization": client.config.use_quantization,
                "test_generation": {
                    "prompt": "The capital of Slovakia is",
                    "selected_token": result.selected_token.token,
                    "selected_probability": f"{result.selected_token.percentage:.2f}%",
                    "top_alternatives": [
                        f"{alt.token} ({alt.percentage:.2f}%)" 
                        for alt in result.top_alternatives[:3]
                    ],
                    "generation_time": f"{result.generation_time:.3f}s"
                }
            }
        else:
            return {
                "status": "error",
                "message": message,
                "model_name": client.config.model_name if client.config else "Unknown",
                "device": "Unknown",
                "quantization": False
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Service test failed: {str(e)}",
            "model_name": "Unknown",
            "device": "Unknown",
            "quantization": False
        }
