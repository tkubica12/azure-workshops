# Troubleshooting Guide

## Quick Reference

| Problem | Quick Fix | Section |
|---------|-----------|---------|
| LLM Service won't start | Check GPU memory, try CPU mode | [Service Issues](#service-issues) |
| Slow token generation | Use GPU, reduce context length | [Performance](#performance-issues) |
| Model download fails | Check Hugging Face auth | [Model Issues](#model-download-issues) |
| Connection errors | Verify service is running on port 8001 | [Connection Issues](#connection-issues) |
| UI not responsive | Refresh page, check service status | [UI Issues](#user-interface-issues) |

## Service Issues

### LLM Service Won't Start

**Symptoms:**
- Error when running `uvicorn main:app`
- Service crashes immediately
- Port 8001 not accessible

**Solutions:**

1. **Check GPU Memory**:
   ```bash
   # Check GPU memory usage
   nvidia-smi
   
   # If GPU memory is full, try CPU mode
   # In llm_service/.env:
   DEVICE=cpu
   ```

2. **Verify Dependencies**:
   ```bash
   cd llm_service
   uv run python -c "import torch; print(torch.cuda.is_available())"
   uv run python -c "import transformers; print(transformers.__version__)"
   ```

3. **Check Hugging Face Authentication**:
   ```bash
   huggingface-cli whoami
   # If not logged in:
   huggingface-cli login
   ```

4. **Try Manual Model Loading**:
   ```bash
   cd llm_service
   uv run python -c "
   from transformers import AutoTokenizer, AutoModelForCausalLM
   tokenizer = AutoTokenizer.from_pretrained('google/gemma-2-2b')
   model = AutoModelForCausalLM.from_pretrained('google/gemma-2-2b')
   print('Model loaded successfully')
   "
   ```

### Main Application Won't Start

**Symptoms:**
- Reflex app fails to start
- Frontend not accessible on port 3000
- Backend connection errors

**Solutions:**

1. **Check Dependencies**:
   ```bash
   cd token_visualizer
   uv run reflex --version
   uv run python -c "import reflex as rx; print(rx.__version__)"
   ```

2. **Clear Reflex Cache**:
   ```bash
   rm -rf .web/
   uv run reflex init  # Reinitialize if needed
   ```

3. **Check Port Availability**:
   ```bash
   # Windows
   netstat -ano | findstr :3000
   netstat -ano | findstr :8000
   
   # macOS/Linux
   lsof -i :3000
   lsof -i :8000
   ```

## Model Download Issues

### Download Fails or Stalls

**Symptoms:**
- Model download stops partway
- "Connection timeout" errors
- "Access denied" errors

**Solutions:**

1. **Verify Hugging Face Access**:
   ```bash
   # Check if you can access the model page
   curl -H "Authorization: Bearer YOUR_HF_TOKEN" \
        https://huggingface.co/api/models/google/gemma-2-2b
   ```

2. **Manual Download**:
   ```bash
   # Download using huggingface-cli
   huggingface-cli download google/gemma-2-2b --local-dir ./models/gemma-2-2b
   ```

3. **Check Disk Space**:
   ```bash
   # Ensure at least 5GB free space
   df -h  # Unix/macOS
   # or check Windows disk space in File Explorer
   ```

4. **Network Issues**:
   - Try different internet connection
   - Check corporate firewall settings
   - Use VPN if in restricted network

### Model Loading Errors

**Symptoms:**
- "Model not found" errors
- "Incompatible model format" errors
- Memory allocation failures

**Solutions:**

1. **Check Model Path**:
   ```python
   # In llm_service, verify model location
   import os
   from transformers import AutoTokenizer
   
   model_path = "google/gemma-2-2b"
   # or local path if downloaded manually
   
   try:
       tokenizer = AutoTokenizer.from_pretrained(model_path)
       print("Model path is correct")
   except Exception as e:
       print(f"Error: {e}")
   ```

2. **Memory Issues**:
   ```bash
   # Check available RAM
   free -h  # Linux
   # or Activity Monitor on macOS, Task Manager on Windows
   
   # If insufficient memory, try:
   # 1. Close other applications
   # 2. Use CPU instead of GPU
   # 3. Enable model quantization (in development)
   ```

## Performance Issues

### Slow Token Generation

**Symptoms:**
- Token generation takes >10 seconds
- UI becomes unresponsive
- High CPU/memory usage

**Solutions:**

1. **Enable GPU Acceleration**:
   ```bash
   # Verify CUDA is available
   uv run python -c "import torch; print(torch.cuda.is_available())"
   
   # If False, install CUDA-enabled PyTorch
   uv add torch --index https://download.pytorch.org/whl/cu118
   ```

2. **Optimize Model Settings**:
   ```env
   # In llm_service/.env
   MAX_LENGTH=1024  # Reduce from 2048
   BATCH_SIZE=1     # Ensure single batch processing
   ```

3. **Monitor Resource Usage**:
   ```bash
   # GPU monitoring
   nvidia-smi -l 1
   
   # CPU/Memory monitoring
   htop  # Linux/macOS
   # or Task Manager on Windows
   ```

### High Memory Usage

**Symptoms:**
- System becomes sluggish
- Out of memory errors
- Other applications crash

**Solutions:**

1. **Use CPU Mode** (reduces VRAM usage):
   ```env
   # In llm_service/.env
   DEVICE=cpu
   ```

2. **Enable Memory Optimization**:
   ```python
   # In model loading code (future enhancement)
   model = AutoModelForCausalLM.from_pretrained(
       model_name,
       torch_dtype=torch.float16,  # Use half precision
       device_map="auto",          # Automatic device placement
       low_cpu_mem_usage=True      # Optimize CPU memory
   )
   ```

3. **Restart Services Periodically**:
   ```bash
   # Memory can accumulate over time
   # Restart LLM service every few hours
   ```

## Connection Issues

### Service Connection Failures

**Symptoms:**
- "Connection refused" errors
- Timeouts when calling LLM service
- UI shows "Service unavailable"

**Solutions:**

1. **Verify Service is Running**:
   ```bash
   # Check if service is listening
   curl http://localhost:8001/health
   
   # Should return: {"status": "healthy"}
   ```

2. **Check Port Configuration**:
   ```env
   # In token_visualizer/.env
   LLM_SERVICE_URL=http://localhost:8001
   
   # In llm_service/.env  
   PORT=8001
   HOST=0.0.0.0  # Important for local connections
   ```

3. **Firewall Issues**:
   ```bash
   # Windows: Allow Python through firewall
   # macOS/Linux: Check iptables rules
   
   # Test with curl
   curl -v http://localhost:8001/health
   ```

4. **Network Binding Problems**:
   ```bash
   # Try different host binding
   uvicorn main:app --host 127.0.0.1 --port 8001
   # or
   uvicorn main:app --host 0.0.0.0 --port 8001
   ```

## User Interface Issues

### UI Not Loading or Responding

**Symptoms:**
- Blank white page
- Buttons don't respond
- JavaScript errors in browser console

**Solutions:**

1. **Check Browser Console**:
   - Open Developer Tools (F12)
   - Look for JavaScript errors
   - Note any network request failures

2. **Clear Browser Cache**:
   ```
   # Chrome: Ctrl+Shift+Delete
   # Firefox: Ctrl+Shift+Delete
   # Safari: Cmd+Option+E
   ```

3. **Try Different Browser**:
   - Test with Chrome, Firefox, Safari, Edge
   - Disable browser extensions temporarily

4. **Verify Reflex is Running**:
   ```bash
   # Should see both frontend and backend running
   # Frontend: http://localhost:3000
   # Backend: http://localhost:8000
   ```

### WebSocket Connection Issues

**Symptoms:**
- State updates don't reflect in UI
- Clicking buttons has no effect
- "Connection lost" messages

**Solutions:**

1. **Check WebSocket Connection**:
   - Browser Developer Tools → Network → WS
   - Should see active WebSocket connection
   - Look for connection errors

2. **Restart Reflex App**:
   ```bash
   # Stop with Ctrl+C, then restart
   uv run reflex run
   ```

3. **Check for Proxy Issues**:
   - Corporate networks sometimes block WebSocket
   - Try from different network
   - Check proxy settings

## Educational Issues

### Unexpected or Confusing Results

**Symptoms:**
- Model gives unexpected predictions
- Probabilities seem wrong
- Biased or inappropriate outputs

**Educational Solutions:**

1. **Explain Model Limitations**:
   - Models reflect training data biases
   - Predictions are statistical, not factual
   - Context heavily influences outputs

2. **Use as Teaching Moments**:
   - Discuss why certain predictions occur
   - Show how prompt changes affect results
   - Demonstrate importance of AI literacy

3. **Provide Better Examples**:
   - Start with clear, unambiguous prompts
   - Use educational content appropriate for audience
   - Prepare example prompts that demonstrate concepts well

### Students Having Difficulty Understanding

**Symptoms:**
- Confusion about probabilities
- Difficulty with interface
- Not grasping educational concepts

**Solutions:**

1. **Simplify Introduction**:
   - Start with temperature = 0.0 (deterministic)
   - Use obvious examples: "The capital of France is..."
   - Explain one concept at a time

2. **Provide Guided Exercises**:
   - Follow the structured exercises in User Guide
   - Use comparison mode to show differences
   - Demonstrate cause and effect clearly

3. **Visual Learning Aids**:
   - Use color coding explanation
   - Show probability bar meanings
   - Relate to familiar concepts (weather prediction, etc.)

## Advanced Troubleshooting

### Service Debugging

**Enable Debug Logging**:
```env
# In llm_service/.env
LOG_LEVEL=debug
```

**Check Service Logs**:
```bash
# Run service with verbose output
uvicorn main:app --host 0.0.0.0 --port 8001 --log-level debug
```

**Test API Directly**:
```bash
# Test generate endpoint
curl -X POST "http://localhost:8001/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "The capital of France is",
       "temperature": 1.0,
       "max_tokens": 1,
       "top_k": 5
     }'
```

### Reflex Debugging

**Enable Reflex Debug Mode**:
```bash
# Run with debug logging
uv run reflex run --loglevel debug
```

**Check Backend State**:
```python
# Add debug prints in state methods
def generate_tokens(self):
    print(f"Current state: {self.current_text}")
    print(f"Temperature: {self.temperature}")
    # ... rest of method
```

### System Diagnostics

**Check Python Environment**:
```bash
# Verify Python version and packages
python --version
uv run pip list | grep -E "(torch|transformers|reflex)"
```

**Check System Resources**:
```bash
# CPU usage
top -p $(pgrep -f "uvicorn\|reflex")

# Memory usage
ps aux | grep -E "(uvicorn|reflex)" | awk '{print $6}'

# GPU usage (if applicable)
nvidia-smi --query-gpu=memory.used,memory.total --format=csv
```

## Getting Help

### Self-Help Resources

1. **Documentation**: Check README.md and docs/ folder
2. **Configuration Test**: Use built-in configuration test page
3. **Logs**: Always check service logs for error details
4. **System Monitor**: Watch resource usage during problems

### Reporting Issues

When reporting problems, include:

1. **Environment Info**:
   - Operating system and version
   - Python version
   - GPU/CPU specifications
   - Available memory

2. **Steps to Reproduce**:
   - Exact commands run
   - Configuration settings used
   - Input that caused the problem

3. **Error Messages**:
   - Complete error text
   - Service logs
   - Browser console errors

4. **Expected vs. Actual**:
   - What you expected to happen
   - What actually happened
   - Screenshots if applicable

### Emergency Workarounds

**Complete Reset**:
```bash
# Stop all services
# Clear all caches and restart

# LLM Service
cd llm_service
rm -rf __pycache__ .venv
uv sync

# Main App  
cd ../token_visualizer
rm -rf .web __pycache__ .venv
uv sync
uv run reflex init
```

**Minimal Working Setup**:
```bash
# Use CPU-only mode for maximum compatibility
echo "DEVICE=cpu" > llm_service/.env
echo "LLM_SERVICE_URL=http://localhost:8001" > token_visualizer/.env
```

Remember: Most issues are environment-related and can be resolved by checking dependencies, authentication, and resource availability.
