"""Gemma model manager for the LLM service."""

import asyncio
import math
import time
import warnings
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

from config import settings


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


class GemmaModelManager:
    """Singleton model manager for Gemma 2 2B model with efficient resource management."""
    
    def __init__(self):
        """Initialize the model manager."""
        self.tokenizer: Optional[AutoTokenizer] = None
        self.model: Optional[AutoModelForCausalLM] = None
        self.device: Optional[str] = None
        self._is_initialized = False
        self._initialization_lock = asyncio.Lock()
        
        # Suppress some warnings for cleaner output
        warnings.filterwarnings("ignore", category=UserWarning)
    
    def _detect_device(self) -> str:
        """Detect the best available device for inference."""
        if settings.device == "auto":
            if torch.cuda.is_available():
                device = "cuda"
                print(f"🚀 Using CUDA: {torch.cuda.get_device_name(0)}")
                memory_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
                print(f"💾 GPU memory: {memory_gb:.1f} GB")
            else:
                device = "cpu"
                print("⚠️  CUDA not available, using CPU")
        else:
            device = settings.device
        
        return device
    
    def _setup_quantization_config(self) -> Optional[BitsAndBytesConfig]:
        """Set up quantization configuration if enabled."""
        if not settings.use_quantization:
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
    
    async def initialize_async(self) -> Tuple[bool, str]:
        """Initialize the model asynchronously."""
        async with self._initialization_lock:
            if self._is_initialized:
                return True, "Model already initialized"
            
            try:
                print(f"🔄 Loading tokenizer: {settings.model_name}")
                # Run in executor to avoid blocking the event loop
                loop = asyncio.get_event_loop()
                
                self.tokenizer = await loop.run_in_executor(
                    None,
                    lambda: AutoTokenizer.from_pretrained(
                        settings.model_name,
                        token=settings.hf_token
                    )
                )
                
                print(f"🔄 Loading model: {settings.model_name}")
                self.device = self._detect_device()
                
                start_time = time.time()
                quantization_config = self._setup_quantization_config()
                
                # Load model with or without quantization
                if quantization_config is not None:
                    self.model = await loop.run_in_executor(
                        None,
                        lambda: AutoModelForCausalLM.from_pretrained(
                            settings.model_name,
                            quantization_config=quantization_config,
                            device_map="auto",
                            low_cpu_mem_usage=True,
                            token=settings.hf_token
                        )
                    )
                else:
                    # Fallback to standard loading
                    self.model = await loop.run_in_executor(
                        None,
                        lambda: AutoModelForCausalLM.from_pretrained(
                            settings.model_name,
                            device_map="auto" if self.device == "cuda" else None,
                            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                            low_cpu_mem_usage=True,
                            token=settings.hf_token
                        )
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
    
    def is_ready(self) -> bool:
        """Check if the model is ready for inference."""
        return self._is_initialized and self.model is not None and self.tokenizer is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        if not self.is_ready():
            return {
                "status": "not_ready",
                "model_name": settings.model_name,
                "device": "unknown",
                "quantization": settings.use_quantization
            }
        
        total_params = sum(p.numel() for p in self.model.parameters())
        params_billions = total_params / 1e9
        
        return {
            "status": "ready",
            "model_name": settings.model_name,
            "device": self.device,
            "quantization": settings.use_quantization,
            "parameters_billions": round(params_billions, 2),
            "memory_efficient": settings.use_quantization
        }
    
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
    
    async def generate_with_logprobs(
        self,
        prompt: str,
        max_tokens: int = None,
        temperature: float = None,
        top_logprobs: int = None
    ) -> TokenGenerationResult:
        """Generate text with probability information for next token.
        
        Args:
            prompt: Input text prompt
            max_tokens: Number of tokens to generate (defaults to service setting)
            temperature: Sampling temperature (defaults to service setting)
            top_logprobs: Number of top alternative tokens to return (defaults to service setting)
            
        Returns:
            TokenGenerationResult with generated text and probabilities
        """
        if not self.is_ready():
            raise RuntimeError("Model not ready. Please wait for initialization to complete.")
        
        # Use defaults from settings if not provided
        max_tokens = max_tokens or settings.default_max_new_tokens
        temperature = temperature or settings.default_temperature
        top_logprobs = top_logprobs or settings.default_top_k
        
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
    
    async def test_generation(self) -> Dict[str, Any]:
        """Test the model with a simple generation."""
        if not self.is_ready():
            return {
                "status": "error",
                "message": "Model not ready"
            }
        
        try:
            test_prompt = "The capital of France is"
            result = await self.generate_with_logprobs(
                prompt=test_prompt,
                max_tokens=1,
                temperature=0.7,
                top_logprobs=5
            )
            
            return {
                "status": "success",
                "prompt": test_prompt,
                "selected_token": result.selected_token.token,
                "selected_probability": f"{result.selected_token.percentage:.2f}%",
                "top_alternatives": [
                    {
                        "token": alt.token,
                        "probability": f"{alt.percentage:.2f}%"
                    }
                    for alt in result.top_alternatives[:3]
                ],
                "generation_time": f"{result.generation_time:.3f}s"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Test generation failed: {str(e)}"
            }
    
    def cleanup(self):
        """Clean up resources."""
        if self.model is not None:
            del self.model
            self.model = None
        
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        self._is_initialized = False
        print("🧹 Model resources cleaned up")
