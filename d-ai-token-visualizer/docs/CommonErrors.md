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

**Spinner Size Values - CRITICAL:**
- ✅ **CORRECT**: Use only `"1"`, `"2"`, or `"3"` for spinner sizes
- ❌ **WRONG**: `"4"` or higher values - these cause TypeErrors specifically for spinner components

**Colors:**
- ✅ **CORRECT**: Use hex codes `"#1F2937"` or Radix color tokens
- ✅ **CORRECT**: CSS color names `"white"`, `"black"` for basic colors
- ❌ **WRONG**: Undefined color variables or invalid color formats

### Common Error Examples

**Spinner Size Error - NEW:**
```python
# ❌ WRONG - Causes TypeError
rx.spinner(size="4")  # This will fail! Spinner only accepts "1", "2", "3"

# ✅ CORRECT
rx.spinner(size="2")  # Use valid spinner size
```

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

## UI/UX Design Issues

### Layout Consistency Problems

**Problem**: Cards or components having inconsistent widths and misaligned layouts in configuration or test pages.

**Root Cause**: Missing `width="100%"` property on card components and improper container alignment settings.

**Solution Pattern:**
```python
# ✅ CORRECT - Consistent card layout
def card_component() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Card content...
            spacing="4",
            align="stretch",
            width="100%"
        ),
        background="white",
        border="1px solid #E5E7EB",
        border_radius="0.5rem",
        padding="1.5rem",
        box_shadow="0 1px 3px 0 rgba(0, 0, 0, 0.1)",
        width="100%"  # CRITICAL - ensures consistent width
    )

# ✅ CORRECT - Container layout
def page_layout() -> rx.Component:
    return rx.container(
        rx.vstack(
            card1(),
            card2(),
            card3(),
            spacing="6",
            align="stretch",  # Use "stretch" not "center" for consistent width
            width="100%"
        ),
        max_width="1000px",  # Appropriate max width
        center_content=True
    )
```

**Prevention**:
1. Always add `width="100%"` to card components
2. Use `align="stretch"` in container VStacks for consistent card widths
3. Set appropriate `max_width` on containers (typically 800px-1200px)

### State Management UI Display Issues

**Problem**: API responses stored in state not displaying properly in UI components.

**Root Cause**: Complex nested state objects don't bind well to Reflex components. Dictionary access patterns like `state.result["key"]["subkey"]` often fail in UI rendering.

**Solution Pattern:**
```python
# ❌ WRONG - Complex nested state access
class APIState(rx.State):
    test_result: Dict[str, Any] = None

# In UI - this often fails:
rx.text(APIState.test_result["response"]["token"])

# ✅ CORRECT - Flattened state properties
class APIState(rx.State):
    test_result: Optional[Dict[str, Any]] = None
    # Individual fields for UI binding
    result_token: str = ""
    result_probability: str = ""
    result_alternatives: List[Dict[str, str]] = []
    
    def set_results(self, api_response):
        # Store both complex and simple versions
        self.test_result = api_response
        self.result_token = api_response.token
        self.result_probability = f"{api_response.probability:.2f}%"

# In UI - this works reliably:
rx.text(APIState.result_token)
rx.text(APIState.result_probability)
```

**Prevention**:
1. Store complex API responses in state for debugging
2. Also store flattened, UI-friendly versions of key data
3. Use simple state property binding in UI components
4. Test state updates immediately after implementation

## Reflex State Variable Operations - CRITICAL

### The Problem
Reflex state variables (Var objects) cannot be used with Python's built-in functions like `len()`, `str()`, `int()`, etc. These will cause TypeErrors at compilation time.

### Critical Rules - ALWAYS FOLLOW

**Length Operations:**
- ✅ **CORRECT**: Use `.length()` method on Reflex state variables
- ❌ **WRONG**: Using `len()` on state variables causes TypeError

**String Operations:**
- ✅ **CORRECT**: Use `.to(str)` or string methods on Reflex vars
- ❌ **WRONG**: Using `str()` on state variables causes TypeError

**Type Conversions:**
- ✅ **CORRECT**: Use `.to(int)`, `.to(float)`, `.to(str)` methods
- ❌ **WRONG**: Using `int()`, `float()`, `str()` on state variables

### Common Error Examples

**Length Check Error:**
```python
# ❌ WRONG - Causes TypeError
rx.cond(
    len(MyState.my_list) > 0,  # This will fail!
    content...
)

# ✅ CORRECT
rx.cond(
    MyState.my_list.length() > 0,  # Use .length() method
    content...
)
```

**String Conversion Error:**
```python
# ❌ WRONG - Causes TypeError
rx.text(str(MyState.my_number))  # This will fail!

# ✅ CORRECT
rx.text(MyState.my_number.to(str))  # Use .to(str) method
```

**Type Conversion Error:**
```python
# ❌ WRONG - Causes TypeError
value = int(MyState.my_string)  # This will fail!

# ✅ CORRECT - In event handler
def my_handler(self, value: str):
    self.my_number = int(value)  # Convert in Python code, not in component
```

### Prevention Strategy

1. **Never Use Built-in Functions**: Avoid `len()`, `str()`, `int()`, `float()` on state variables
2. **Use Var Methods**: Always use `.length()`, `.to()`, and other Var methods
3. **Handle Conversions in Event Handlers**: Do type conversions in Python event handlers, not in components
4. **Check Error Messages**: Look for "Cannot pass a Var to a built-in function" errors

## Reflex Icon Component Issues

### Invalid Icon Names Problem

**Problem**: Using emoji characters or invalid icon names in `rx.icon()` components causes warnings and fallback to default icons.

**Error Pattern**:
```
Warning: Invalid icon tag: 📊. Please use one of the following: a_arrow_down, a_arrow_up, ...
Using 'circle_help' icon instead.
```

**Root Cause**: Reflex uses Lucide icons under the hood and only accepts valid Lucide icon names, not emoji characters or custom strings.

**Solution**:
```python
# ❌ WRONG - Using emoji characters
nav_button(icon="⚡", label="Interactive Generation")
nav_button(icon="📊", label="Live Probability") 
nav_button(icon="🎨", label="Color Visualization")
nav_button(icon="🌳", label="Token Tree")

# ✅ CORRECT - Using valid Lucide icon names
nav_button(icon="zap", label="Interactive Generation")
nav_button(icon="activity", label="Live Probability")
nav_button(icon="palette", label="Color Visualization") 
nav_button(icon="git-branch", label="Token Tree")
```

**Common Valid Icon Names**:
- **Interactive/Action**: `zap`, `play`, `cursor-click`, `hand`, `mouse-pointer`
- **Data/Analytics**: `activity`, `bar-chart`, `line-chart`, `trending-up`, `pie-chart`
- **Visual/Design**: `palette`, `brush`, `eye`, `image`, `color-picker`
- **Structure/Tree**: `git-branch`, `tree-view`, `folder-tree`, `network`
- **Tools/Settings**: `wrench`, `settings`, `tool`, `cog`, `gear`
- **Help/Documentation**: `help-circle`, `book`, `file-text`, `info`, `question-mark`
- **Export/Download**: `download`, `save`, `export`, `archive`, `file-down`

**Prevention**:
1. Always use valid Lucide icon names - check the Reflex documentation
2. Test icons immediately after adding them
3. Use semantic icon names that match the functionality
4. Reference: https://reflex.dev/docs/library/data-display/icon/#icons-list

### Icon Size and Styling

**Correct Icon Usage**:
```python
# ✅ CORRECT - Proper icon component usage
rx.icon(
    "zap",
    size=16,          # Use numeric pixel values
    color="#2563EB",  # Use hex colors or CSS color names
)
```