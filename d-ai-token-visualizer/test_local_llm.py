#!/usr/bin/env python3
"""
Test script to verify local Gemma 2 2B model loading and logits extraction.
This script tests the basic functionality needed for the Token Visualizer before building the main application.
"""

import os
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import time
import warnings
from dotenv import load_dotenv

def load_environment():
    """Load environment variables and validate Hugging Face authentication."""
    load_dotenv()
    
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    if not hf_token or hf_token == "your_hf_token_here":
        print("❌ Error: Missing Hugging Face token!")
        print("📋 To fix this:")
        print("   1. Go to: https://huggingface.co/settings/tokens")
        print("   2. Create a new token with 'Read' permissions")
        print("   3. Accept Gemma 2 license at: https://huggingface.co/google/gemma-2-2b")
        print("   4. Add your token to .env file: HUGGINGFACE_TOKEN=your_actual_token")
        return None
    
    return hf_token
"""
Test script to verify local Gemma 2 2B model loading and logits extraction.
This script tests the basic functionality needed for the Token Visualizer before building the main application.
"""

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import time
import warnings

def test_environment_setup():
    """Test basic environment and dependencies."""
    print("🔧 Testing Environment Setup...")
    
    # Check PyTorch installation
    print(f"✅ PyTorch version: {torch.__version__}")
    
    # Check for bitsandbytes (required for quantization)
    try:
        import bitsandbytes
        print(f"✅ BitsAndBytes available: {bitsandbytes.__version__}")
        quantization_available = True
    except ImportError:
        print("⚠️  BitsAndBytes not available - quantization disabled")
        quantization_available = False
    
    # Check CUDA availability
    if torch.cuda.is_available():
        print(f"🚀 CUDA available: {torch.cuda.get_device_name(0)}")
        print(f"💾 GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        device = "cuda"
    else:
        print("⚠️  CUDA not available, using CPU")
        device = "cpu"
    
    if quantization_available:
        print("⚡ 4-bit quantization enabled - significant memory savings!")
    else:
        print("💡 Install bitsandbytes for quantization: pip install bitsandbytes")
    
    return device

def test_model_loading(device, hf_token):
    """Test Gemma 2 2B model loading with 4-bit quantization."""
    print("\n📥 Testing Model Loading (4-bit Quantized)...")
    
    model_name = "google/gemma-2-2b"
    
    try:
        print(f"🔄 Loading tokenizer: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
        
        print(f"🔄 Loading quantized model: {model_name}")
        print("⚡ Using 4-bit quantization for reduced memory usage...")
        start_time = time.time()
        
        # Set up 4-bit quantization configuration
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )
        
        # Load model with quantization
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=quantization_config,
            device_map="auto",
            low_cpu_mem_usage=True,
            token=hf_token
        )
        
        load_time = time.time() - start_time
        print(f"✅ Quantized model loaded successfully in {load_time:.2f} seconds")
        
        # Get model info
        total_params = sum(p.numel() for p in model.parameters())
        print(f"📊 Model parameters: {total_params / 1e9:.2f}B")
        print(f"💾 Memory efficient: 4-bit quantization (~75% memory reduction)")
        
        return tokenizer, model
        
    except Exception as e:
        print(f"❌ Error loading quantized model: {str(e)}")
        print("💡 Trying fallback to standard loading...")
        
        # Fallback to standard loading if quantization fails
        try:
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map="auto" if device == "cuda" else None,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                low_cpu_mem_usage=True,
                token=hf_token
            )
            
            if device == "cpu":
                model = model.to(device)
                
            print(f"✅ Fallback model loaded successfully")
            return tokenizer, model
        except Exception as fallback_error:
            print(f"❌ Fallback also failed: {str(fallback_error)}")
            return None, None

def test_basic_inference(tokenizer, model, device):
    """Test basic text generation."""
    print("\n🧪 Testing Basic Inference...")
    
    test_prompt = "The capital of France is"
    print(f"📝 Test prompt: '{test_prompt}'")
    
    try:
        # Tokenize input
        inputs = tokenizer(test_prompt, return_tensors="pt")
        if device == "cuda":
            inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Generate with basic settings
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=5,
                do_sample=False,  # Greedy for consistent testing
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode the result
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        new_text = generated_text[len(test_prompt):]
        
        print(f"✅ Generated text: '{generated_text}'")
        print(f"🎯 New tokens: '{new_text}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in basic inference: {str(e)}")
        return False

def test_logits_extraction(tokenizer, model, device):
    """Test logits extraction for next token prediction."""
    print("\n🔍 Testing Logits Extraction...")
    
    test_prompt = "The capital of Slovakia is"
    print(f"📝 Test prompt: '{test_prompt}'")
    
    try:
        # Tokenize input
        inputs = tokenizer(test_prompt, return_tensors="pt")
        if device == "cuda":
            inputs = {k: v.to(device) for k, v in inputs.items()}
        
        print(f"🔢 Input token IDs: {inputs['input_ids'].tolist()[0]}")
        print(f"📏 Input length: {len(inputs['input_ids'][0])} tokens")
        
        # Generate one token with logits
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=1,
                temperature=0.7,
                do_sample=True,
                return_dict_in_generate=True,
                output_scores=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Extract the generated token
        generated_sequence = outputs.sequences[0]
        new_token_id = generated_sequence[-1].item()
        new_token = tokenizer.decode([new_token_id])
        
        print(f"✅ Generated token: '{new_token}' (ID: {new_token_id})")
        
        # Extract logits for the generated token
        if outputs.scores and len(outputs.scores) > 0:
            logits = outputs.scores[0][0]  # First (and only) generated token, first batch item
            
            print(f"📊 Logits shape: {logits.shape}")
            print(f"📈 Vocabulary size: {len(logits)}")
            
            # Convert logits to probabilities
            probabilities = F.softmax(logits, dim=-1)
            
            # Get top-k tokens and probabilities
            top_k = 5
            top_probs, top_indices = torch.topk(probabilities, top_k)
            
            print(f"\n🏆 Top {top_k} next token predictions:")
            for i, (prob, token_id) in enumerate(zip(top_probs, top_indices)):
                token = tokenizer.decode([token_id.item()])
                print(f"  {i+1}. '{token}' - {prob.item()*100:.2f}% (ID: {token_id.item()})")
            
            # Verify the generated token is in top predictions
            generated_prob = probabilities[new_token_id].item()
            print(f"\n🎯 Generated token probability: {generated_prob*100:.2f}%")
            
            return True
        else:
            print("❌ No logits found in output")
            return False
            
    except Exception as e:
        print(f"❌ Error in logits extraction: {str(e)}")
        return False

def test_interactive_generation(tokenizer, model, device):
    """Test interactive token-by-token generation with timing measurements."""
    print("\n🎮 Testing Interactive Generation...")
    
    initial_prompt = "What is the capital of Slovakia?"
    current_text = initial_prompt
    max_tokens = 3
    
    print(f"🎬 Starting with: '{current_text}'")
    
    try:
        total_generation_start = time.time()
        first_token_time = None
        generation_times = []
        
        for step in range(max_tokens):
            print(f"\n--- Step {step + 1} ---")
            step_start_time = time.time()
            
            # Tokenize current text
            inputs = tokenizer(current_text, return_tensors="pt")
            if device == "cuda":
                inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # First, get the logits for next token prediction (without sampling)
            with torch.no_grad():
                model_outputs = model(**inputs)
                logits = model_outputs.logits[0, -1, :]  # Last token logits
                probabilities = F.softmax(logits, dim=-1)
                top_probs, top_indices = torch.topk(probabilities, 5)
                
                print(f"📍 Current text: '{current_text}'")
                print("🎲 Next token alternatives:")
                for i, (prob, token_id) in enumerate(zip(top_probs, top_indices)):
                    token = tokenizer.decode([token_id.item()])
                    print(f"  {i+1}. '{token}' - {prob.item()*100:.2f}%")
            
            # Now generate one token using sampling (which might pick a different token)
            token_generation_start = time.time()
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=1,
                    temperature=0.8,
                    do_sample=True,
                    return_dict_in_generate=True,
                    output_scores=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            token_generation_end = time.time()
            
            # Get the actually generated token
            generated_sequence = outputs.sequences[0]
            new_token_id = generated_sequence[-1].item()
            new_token = tokenizer.decode([new_token_id])
            
            # Get the probability of the actually generated token
            generated_prob = probabilities[new_token_id].item()
            
            # Add the generated token to current text
            current_text = tokenizer.decode(generated_sequence, skip_special_tokens=True)
            
            step_end_time = time.time()
            step_duration = step_end_time - step_start_time
            token_generation_time = token_generation_end - token_generation_start
            
            # Track timing for first token vs subsequent tokens
            if step == 0:
                first_token_time = step_duration
                print(f"⏱️  Time to first token: {first_token_time:.3f}s")
            else:
                generation_times.append(token_generation_time)
            
            print(f"🎯 Actually generated: '{new_token}' - {generated_prob*100:.2f}% (ID: {new_token_id})")
            print(f"📝 Updated text: '{current_text}'")
            print(f"⚡ Token generation time: {token_generation_time:.3f}s")
        
        total_generation_end = time.time()
        total_generation_time = total_generation_end - total_generation_start
        
        print(f"\n🎉 Final generated text: '{current_text}'")
        print(f"\n📊 Performance Metrics:")
        print(f"⏱️  Time to first token: {first_token_time:.3f}s")
        
        if generation_times:
            avg_subsequent_time = sum(generation_times) / len(generation_times)
            tokens_per_second = 1.0 / avg_subsequent_time if avg_subsequent_time > 0 else 0
            print(f"🚀 Average subsequent token time: {avg_subsequent_time:.3f}s")
            print(f"⚡ Tokens per second (after first): {tokens_per_second:.2f} t/s")
        
        print(f"🕐 Total generation time: {total_generation_time:.3f}s")
        overall_tokens_per_second = max_tokens / total_generation_time if total_generation_time > 0 else 0
        print(f"📈 Overall tokens per second: {overall_tokens_per_second:.2f} t/s")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in interactive generation: {str(e)}")
        return False

def main():
    """Main function to run all tests."""
    print("🚀 Gemma 2 Local LLM Test for Token Visualizer")
    print("=" * 60)
    
    # Suppress some warnings for cleaner output
    warnings.filterwarnings("ignore", category=UserWarning)
    
    # Test 0: Load environment and validate HF token
    hf_token = load_environment()
    if hf_token is None:
        print("\n❌ Authentication setup failed. Cannot proceed with tests.")
        return False
    
    print(f"✅ Hugging Face token loaded successfully")
    
    # Test 1: Environment setup
    device = test_environment_setup()
    
    # Test 2: Model loading
    tokenizer, model = test_model_loading(device, hf_token)
    if tokenizer is None or model is None:
        print("\n❌ Model loading failed. Cannot proceed with further tests.")
        return False
    
    # Test 3: Basic inference
    if not test_basic_inference(tokenizer, model, device):
        print("\n❌ Basic inference failed.")
        return False
    
    # Test 4: Logits extraction
    if not test_logits_extraction(tokenizer, model, device):
        print("\n❌ Logits extraction failed.")
        return False
    
    # Test 5: Interactive generation
    if not test_interactive_generation(tokenizer, model, device):
        print("\n❌ Interactive generation failed.")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 All tests passed! Gemma 2 is ready for Token Visualizer.")
    print("✅ Next steps:")
    print("   1. Update project dependencies in pyproject.toml")
    print("   2. Create local_llm.py service module")
    print("   3. Integrate with Reflex application")
    print("   4. Build interactive token generation interface")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n📋 Troubleshooting:")
        print("   • Make sure you have accepted Gemma 2 license on Hugging Face")
        print("   • Install required dependencies:")
        print("     pip install torch transformers accelerate bitsandbytes")
        print("   • For GPU: Install CUDA-compatible PyTorch")
        print("   • For CPU: Ensure sufficient RAM (4GB+ with quantization)")
        print("   • BitsAndBytes enables 4-bit quantization for memory efficiency")
        exit(1)
