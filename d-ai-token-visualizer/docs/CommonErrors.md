# Common Errors

## Overview

This document contains common errors encountered during development of the Token Visualizer project. These patterns and guidelines should be considered for every phase of development to avoid recurring issues. Use this document as reference when implementing new features or debugging issues.

## Reflex Component Props - CRITICAL

### The Problem
Reflex uses Radix UI components under the hood and enforces strict prop type validation. Using incorrect prop types will cause TypeErrors at runtime and prevent components from rendering.

### Critical Rules - ALWAYS FOLLOW

**Spacing Values:**
- ✅ **CORRECT**: Use string literals `"0"`, `"1"`, `"2"`, `"3"`, `"4"`, `"5"`, `"6"`, `"7"`, `"8"`, `"9"`
- ❌ **WRONG**: CSS values like `"0.5rem"`, `"1rem"`, `"2rem"`, `"24px"` - these cause TypeErrors

**Size Values:**
- ✅ **CORRECT**: Use string literals `"1"`, `"2"`, `"3"`, `"4"` for button sizes, heading sizes, etc.
- ❌ **WRONG**: Old size values like `"sm"`, `"md"`, `"lg"`, `"xl"`

**Colors:**
- ✅ **CORRECT**: Use hex codes `"#1F2937"` or Radix color tokens
- ✅ **CORRECT**: CSS color names `"white"`, `"black"` for basic colors
- ❌ **WRONG**: Undefined color variables or invalid color formats

### Common Error Examples

**VStack/HStack Spacing Error:**
```python
# ❌ WRONG - Causes TypeError
rx.vstack(
    components...,
    spacing="1rem"  # This will fail!
)

# ✅ CORRECT
rx.vstack(
    components...,
    spacing="4"     # Use string literal
)
```

**Button Size Error:**
```python
# ❌ WRONG - Causes TypeError  
rx.button(
    "Click me",
    size="lg"       # This will fail!
)

# ✅ CORRECT
rx.button(
    "Click me", 
    size="4"        # Use string literal
)
```

**Grid Columns Error:**
```python
# ❌ WRONG - Causes TypeError
rx.grid(
    components...,
    columns=3       # This will fail!
)

# ✅ CORRECT
rx.grid(
    components...,
    columns="3"     # Use string literal
)
```

### Prevention Strategy

1. **Always Check Existing Code**: Before creating new components, look at working examples in the codebase
2. **Use String Literals**: When in doubt, use string literals for numeric prop values
3. **Test Immediately**: Run the application after adding new components to catch prop errors early
4. **Reference This Document**: Keep this guide open when developing Reflex components

## Import Structure - Reflex Applications

### The Problem
Reflex has specific requirements for module structure and imports that differ from standard Python applications.

### Critical Rules

**App Structure:**
- ✅ **CORRECT**: `app_name/app_name.py` pattern (e.g., `token_visualizer/token_visualizer.py`)
- ❌ **WRONG**: `app_name/__init__.py` as main app file

**Import Pattern:**
```python
# ✅ CORRECT - Relative imports within app
from .components.layout import app_layout
from .state.ui_state import NavigationState

# ✅ CORRECT - Reflex import
import reflex as rx
```

## Configuration and Environment Variables

### The Problem
Environment variable loading and configuration validation needs to happen before Reflex app initialization.

### Best Practices

**Environment File Structure:**
```bash
# ✅ CORRECT - .env file format
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
USE_AZURE_DEFAULT_CREDENTIALS=true
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1-nano
AZURE_OPENAI_API_VERSION=2024-02-01
```

**Configuration Loading:**
```python
# ✅ CORRECT - Load config before using
from dotenv import load_dotenv
load_dotenv()  # Call this first

# Then access environment variables
import os
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
```

## Azure OpenAI Integration

### Authentication Patterns

**Azure Default Credentials (Recommended):**
```python
# ✅ CORRECT - AAD Authentication
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(
    credential, 
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version=api_version
)
```

**API Key Authentication (Fallback):**
```python
# ✅ CORRECT - API Key Authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_version
)
```

### Logprobs Usage

**Correct Logprobs Request:**
```python
# ✅ CORRECT - Logprobs with Azure OpenAI
response = client.chat.completions.create(
    model=deployment_name,
    messages=[{"role": "user", "content": prompt}],
    max_tokens=1,
    temperature=0.7,
    logprobs=True,        # Enable logprobs
    top_logprobs=5        # Get top 5 alternatives
)
```

**Logprobs Response Parsing:**
```python
# ✅ CORRECT - Safe logprobs extraction
if response.choices[0].logprobs and response.choices[0].logprobs.content:
    logprobs_data = response.choices[0].logprobs.content[0]
    
    # Convert logprob to probability
    probability = math.exp(logprobs_data.logprob)
    percentage = probability * 100.0
```

## State Management - Reflex

### State Class Patterns

**Correct State Definition:**
```python
# ✅ CORRECT - Reflex State class
import reflex as rx

class MyState(rx.State):
    # Use type hints
    counter: int = 0
    message: str = ""
    is_loading: bool = False
    
    def increment(self):
        """Event handler methods."""
        self.counter += 1
    
    def set_message(self, msg: str):
        """Event handlers can take parameters."""
        self.message = msg
```

## Development Workflow

### Testing and Verification

1. **Always Test After Changes**: Run `reflex run` after making component changes
2. **Check Browser Console**: Look for JavaScript errors that might indicate prop issues
3. **Verify Responsive Design**: Test on different screen sizes
4. **Test State Updates**: Verify state changes trigger UI updates correctly

### Debugging Tips

1. **Component Prop Errors**: Usually show as TypeErrors mentioning "Invalid var passed for prop"
2. **Import Errors**: Check relative import paths and module structure
3. **State Issues**: Verify event handlers are properly defined and called
4. **API Errors**: Check authentication and endpoint configuration

## References

- **Reflex Documentation**: https://reflex.dev/docs/
- **Radix UI Components**: https://www.radix-ui.com/
- **Azure OpenAI Documentation**: https://docs.microsoft.com/azure/cognitive-services/openai/