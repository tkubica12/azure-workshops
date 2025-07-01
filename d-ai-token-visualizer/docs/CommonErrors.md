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
Reflex state variables (Var objects) cannot be used with Python's built-in functions like `len()`, `str()`, `int()`, etc. More importantly, they cannot be used with Python's boolean operators like `or`, `and`, `not`, or in `if` statements. These will cause VarTypeError at compilation time.

### Critical Rules - ALWAYS FOLLOW

**Boolean Operations:**
- ✅ **CORRECT**: Use `rx.cond()` for conditional logic
- ❌ **WRONG**: Using `if`, `and`, `or`, `not` on state variables causes VarTypeError

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

**String Concatenation Error:**
```python
# ❌ WRONG - rx.concat doesn't exist
rx.text(rx.concat('"', token.token, '"'))  # This will fail!
rx.text(rx.concat("Value: ", rx.format("{:.2f}", value)))  # This will fail!

# ✅ CORRECT - Use f-strings for static content
rx.text(f'"{token.token}"')  # Simple string interpolation
rx.text(f"Value: {value:.2f}")  # Use f-strings with state variables

# ✅ CORRECT - For complex dynamic content, use proper formatting
rx.text(token.token)  # Direct variable reference
```

**Lambda Function Conditionals Error:**
```python
# ❌ WRONG - Causes VarTypeError in lambda
on_click=lambda: on_token_select(index) if on_token_select else None  # This will fail!

# ✅ CORRECT - Use rx.cond for conditional lambda expressions
on_click=rx.cond(
    on_token_select,
    lambda: on_token_select(index),
    lambda: None
)
```

**VarTypeError - Boolean Operations:**
```python
# ❌ WRONG - Causes VarTypeError
def my_component(alternatives=None):
    alternatives = alternatives or []  # This will fail with state vars!
    return rx.text("Hello")

# ❌ WRONG - Causes VarTypeError  
rx.text(
    "Loading..." if MyState.is_loading else "Ready"  # This will fail!
)

# ❌ WRONG - Causes VarTypeError
rx.button(
    "Button",
    disabled=MyState.is_loading or not MyState.is_ready  # This will fail!
)

# ✅ CORRECT - Use rx.cond properly
def my_component(alternatives=None):
    # Handle None case in the component calling this one
    return rx.cond(
        alternatives,
        rx.text("Has alternatives"),
        rx.text("No alternatives")
    )

# ✅ CORRECT - Use rx.cond for conditional text
rx.cond(
    MyState.is_loading,
    rx.text("Loading..."),
    rx.text("Ready")
)

# ✅ CORRECT - Use bitwise operators for complex conditions
rx.button(
    "Button",
    disabled=rx.cond(
        MyState.is_loading | ~MyState.is_ready,
        True,
        False
    )
)
```

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

### Component Design Patterns

**Handling Optional State Variables:**
```python
# ❌ WRONG - Cannot use `or` with state variables
def my_component(alternatives=None):
    alternatives = alternatives or []  # VarTypeError!
    return content

# ✅ CORRECT - Handle None case in parent component
def parent_component():
    return rx.cond(
        MyState.alternatives,
        my_component(alternatives=MyState.alternatives),
        rx.text("No data available")
    )

def my_component(alternatives):
    # Assume alternatives is always valid here
    return rx.foreach(alternatives, lambda item: rx.text(item))
```

### Prevention Strategy

1. **Never Use Built-in Functions**: Avoid `len()`, `str()`, `int()`, `float()` on state variables
2. **Never Use Boolean Operators**: Avoid `or`, `and`, `not`, `if` on state variables
3. **Use Var Methods**: Always use `.length()`, `.to()`, and other Var methods
4. **Handle Conversions in Event Handlers**: Do type conversions in Python event handlers, not in components
5. **Use rx.cond for Conditionals**: Always use `rx.cond()` for conditional rendering with state variables
6. **Check Error Messages**: Look for "Cannot convert Var to bool" or "VarTypeError" errors

### Error Message Patterns

**VarTypeError:**
```
VarTypeError: Cannot convert Var 'state_variable_name' to bool for use with `if`, `and`, `or`, and `not`. 
Instead use `rx.cond` and bitwise operators `&` (and), `|` (or), `~` (invert).
```

**TypeError:**
```
TypeError: Cannot pass a Var to a built-in function like len(), str(), etc.
```

When you see these errors, immediately look for Python operators being used on Reflex state variables and replace them with the appropriate Reflex methods.

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

## Reflex State Management - CRITICAL

### The Problem
Reflex State classes have built-in methods that cannot be overridden or shadowed by event handlers. Using these names will cause EventHandlerShadowsBuiltInStateMethodError.

### Critical Rules - ALWAYS FOLLOW

**Reserved Method Names - NEVER USE:**
- ❌ **WRONG**: `reset` - This is a built-in State method
- ❌ **WRONG**: `process` - Built-in State method 
- ❌ **WRONG**: `preprocess` - Built-in State method
- ❌ **WRONG**: `postprocess` - Built-in State method

**Correct Naming:**
- ✅ **CORRECT**: `reset_counter`, `reset_session`, `clear_data` instead of `reset`
- ✅ **CORRECT**: `process_data`, `handle_data` instead of `process`

### Common Error Examples

**EventHandlerShadowsBuiltInStateMethodError:**
```python
# ❌ WRONG - Causes EventHandlerShadowsBuiltInStateMethodError
class MyState(rx.State):
    count: int = 0
    
    def reset(self):  # This will fail!
        self.count = 0

# ✅ CORRECT
class MyState(rx.State):
    count: int = 0
    
    def reset_counter(self):  # Use descriptive name
        self.count = 0
```

**Var Length Error:**
```python
# ❌ WRONG - Cannot use len() on Reflex Vars
rx.text(f"Count: {len(MyState.items)}")  # This will fail!

# ✅ CORRECT - Use .length() method
rx.text(f"Count: {MyState.items.length()}")
```

**Event Handler Direct List Modification:**
```python
# ❌ WRONG - Cannot call append() directly in lambda
rx.button(
    "Add Item",
    on_click=lambda: MyState.items.append("new_item")  # This will fail!
)

# ✅ CORRECT - Create proper event handler method
class MyState(rx.State):
    items: list[str] = []
    
    def add_item(self):
        self.items.append("new_item")

rx.button(
    "Add Item", 
    on_click=MyState.add_item  # Use event handler method
)
```

**Input Binding:**
```python
# ❌ WRONG - Missing on_change for input binding
rx.input(
    value=MyState.text,  # This won't update the state
    placeholder="Enter text..."
)

# ✅ CORRECT - Use on_change for two-way binding
rx.input(
    value=MyState.text,
    on_change=MyState.set_text,  # Add event handler for changes
    placeholder="Enter text..."
)
```

### Prevention Strategy

1. **Check Built-in Methods**: Always check if a method name might conflict with built-in State methods
2. **Use Descriptive Names**: Instead of generic names like `reset`, use specific names like `reset_counter`
3. **Use Event Handlers**: Never try to modify state directly in UI components - always use event handler methods
4. **Use .length()**: For Reflex Vars that are lists, use `.length()` instead of `len()`
5. **Test Immediately**: Run the application after adding new state methods to catch naming conflicts early

## LLM Service API Endpoints - CRITICAL

### The Problem
The LLM service has a mixed endpoint structure that can cause 404 errors if not used correctly.

### Critical Rules - ALWAYS FOLLOW

**Health Check Endpoint:**
- ✅ **CORRECT**: Use `/health` (root level endpoint)
- ❌ **WRONG**: Using `/api/v1/health` will return 404

**Other API Endpoints:**
- ✅ **CORRECT**: Use `/api/v1/` prefix for status, generate, and test endpoints
- ❌ **WRONG**: Omitting the prefix will return 404

**Complete Endpoint List:**
```
GET  /health                    - Service health check (root level)
GET  /api/v1/status             - Model loading status and info  
POST /api/v1/generate           - Token generation with probabilities
POST /api/v1/test               - Simple test generation endpoint
```

**Why This Structure:**
- The `/health` endpoint is defined directly in main.py for quick health checks
- All other endpoints are routed through the API router with `/api/v1` prefix
- This allows for API versioning while keeping health checks at root level

## LLM Temperature Handling - CRITICAL

### The Problem
Setting temperature to exactly 0.0 in LLM APIs causes numerical instability leading to NaN (Not a Number) values in probability calculations. This results in JSON serialization errors: "Out of range float values are not JSON compliant: nan".

### Root Cause
When temperature=0, the softmax calculation `logits / temperature` results in division by zero or extreme values that cause mathematical overflow, producing NaN values that cannot be serialized to JSON.

### Critical Solution - ALWAYS IMPLEMENT

**Frontend Temperature Handling:**
```python
# ✅ CORRECT - Convert 0 to small positive number
effective_temperature = self.temperature if self.temperature > 0 else 0.001

# Never send exactly 0.0 to API
result = await client.generate_tokens_with_probabilities(
    temperature=effective_temperature  # Use converted value
)
```

**Backend Temperature Validation:**
```python
# ✅ CORRECT - Backend safety check
if temperature <= 0.001:
    temperature = 0.001  # Use small positive number for numerical stability
    print(f"INFO: Temperature adjusted to 0.001 for numerical stability")

# Apply temperature scaling safely
scaled_logits = logits / temperature  # No division by zero
```

**User Experience Handling:**
```python
# ✅ CORRECT - Show user 0.0, use 0.001 internally
rx.text(f"Temperature: {self.temperature:.1f}")  # Shows "0.0" to user
# But internally use effective_temperature = 0.001 for API calls
```

### Why 0.001 Works
- **Small Enough**: Still provides deterministic behavior (always picks highest probability token)
- **Large Enough**: Avoids numerical instability and NaN generation
- **JSON Safe**: Produces valid floating-point numbers that serialize correctly
- **Mathematically Sound**: Maintains proper softmax distribution calculations

### Prevention Strategy
1. **Always validate temperature input** before sending to any LLM API
2. **Implement both frontend and backend checks** for redundancy
3. **Use consistent minimum value** (0.001) across all components
4. **Add logging** when temperature adjustments occur
5. **Test with temperature=0** to verify no JSON errors

### Error Symptoms
If you see these errors, check temperature handling:
```
ValueError: Out of range float values are not JSON compliant: nan
TypeError: Object of type float32 is not JSON serializable
RuntimeError: Expected finite float values, got nan
```

### Testing Checklist
- ✅ Test with temperature=0.0 (should convert to 0.001)
- ✅ Test with temperature=0.1-2.0 (should use exact values)
- ✅ Verify no NaN values in API responses
- ✅ Confirm JSON serialization works correctly
- ✅ Check that deterministic behavior works (temperature near 0)