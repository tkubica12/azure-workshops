# Developer Documentation

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [LLM Service API](#llm-service-api)
3. [Component Documentation](#component-documentation)
4. [State Management](#state-management)
5. [Development Setup](#development-setup)
6. [Contributing Guidelines](#contributing-guidelines)
7. [Testing](#testing)

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────┐
│           Frontend (Reflex)             │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │  Mode 1 │ │  Mode 2 │ │  Mode 3 │   │
│  │Interactive│ │Comparison│ │  Tree   │   │
│  └─────────┘ └─────────┘ └─────────┘   │
│  ┌─────────────────────────────────────┐ │
│  │     Shared Components               │ │
│  │  ┌─────────┐ ┌─────────┐ ┌───────┐ │ │
│  │  │ Layout  │ │  Token  │ │ Color │ │ │
│  │  │         │ │ Display │ │ Coded │ │ │
│  │  └─────────┘ └─────────┘ └───────┘ │ │
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
                    │ HTTP API
                    ▼
┌─────────────────────────────────────────┐
│         LLM Service (FastAPI)           │
│  ┌─────────────────────────────────────┐ │
│  │           API Layer                 │ │
│  │  /generate  /health  /status        │ │
│  └─────────────────────────────────────┘ │
│  ┌─────────────────────────────────────┐ │
│  │         Model Layer                 │ │
│  │     Gemma 2 2B Model Loading       │ │
│  │     Token Generation Logic         │ │
│  │     Probability Calculation        │ │
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Key Design Principles

1. **Separation of Concerns**: UI logic separated from ML inference
2. **Service Isolation**: LLM service can be developed/deployed independently
3. **Educational Focus**: All components designed for learning and exploration
4. **Type Safety**: Comprehensive type hints and validation
5. **Error Handling**: Graceful degradation and user-friendly error messages

### Technology Stack

**Frontend/Backend (Reflex)**
- **Framework**: Reflex (Python full-stack web framework)
- **State Management**: Reflex built-in state system
- **UI Components**: Radix UI via Reflex
- **Styling**: CSS-in-Python with Reflex styling system
- **Real-time Updates**: WebSocket-based state synchronization

**LLM Service (FastAPI)**
- **API Framework**: FastAPI with automatic OpenAPI documentation
- **ML Framework**: Hugging Face Transformers
- **Model**: Google Gemma 2 2B base model
- **Inference**: PyTorch with CUDA/CPU support
- **Async Processing**: Python asyncio for concurrent requests

---

## LLM Service API

### Base URL
```
http://localhost:8001
```

### Authentication
Currently optional. If `API_KEY` is set in environment:
```http
Authorization: Bearer YOUR_API_KEY
```

### Endpoints

#### GET /health
**Description**: Health check endpoint for service monitoring.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-01T12:00:00Z"
}
```

**Status Codes**:
- `200`: Service is healthy
- `503`: Service unavailable (model not loaded)

---

#### GET /status
**Description**: Detailed service and model information.

**Response**:
```json
{
  "service": {
    "status": "running",
    "version": "0.1.0",
    "uptime_seconds": 3600
  },
  "model": {
    "name": "google/gemma-2-2b",
    "loaded": true,
    "device": "cuda:0",
    "memory_usage": {
      "allocated_mb": 4096,
      "cached_mb": 512
    }
  },
  "system": {
    "gpu_available": true,
    "gpu_memory_total": 12288,
    "gpu_memory_free": 8192
  }
}
```

---

#### POST /generate
**Description**: Generate token probabilities for next token prediction.

**Request Body**:
```json
{
  "prompt": "The capital of France is",
  "temperature": 1.0,
  "max_tokens": 1,
  "top_k": 5
}
```

**Request Schema**:
```python
class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="Input text prompt")
    temperature: float = Field(1.0, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: int = Field(1, ge=1, le=100, description="Maximum tokens to generate")
    top_k: int = Field(5, ge=1, le=50, description="Number of top tokens to return")
```

**Response**:
```json
{
  "generated_text": " Paris",
  "tokens": [
    {
      "token": " Paris",
      "probability": 0.8234,
      "percentage": 82.34,
      "logprob": -0.1941
    },
    {
      "token": " Lyon",
      "probability": 0.0892,
      "percentage": 8.92,
      "logprob": -2.4159
    },
    {
      "token": " Marseille",
      "probability": 0.0567,
      "percentage": 5.67,
      "logprob": -2.8693
    },
    {
      "token": " Nice",
      "probability": 0.0234,
      "percentage": 2.34,
      "logprob": -3.7492
    },
    {
      "token": " Bordeaux",
      "probability": 0.0073,
      "percentage": 0.73,
      "logprob": -4.9164
    }
  ],
  "metadata": {
    "model_name": "google/gemma-2-2b",
    "prompt_length": 23,
    "generation_time_ms": 156,
    "temperature_used": 1.0
  }
}
```

**Response Schema**:
```python
class TokenProbability(BaseModel):
    token: str = Field(..., description="Token text")
    probability: float = Field(..., description="Probability (0.0-1.0)")
    percentage: float = Field(..., description="Percentage (0.0-100.0)")
    logprob: float = Field(..., description="Log probability")

class GenerateResponse(BaseModel):
    generated_text: str = Field(..., description="Generated text")
    tokens: List[TokenProbability] = Field(..., description="Top-k token probabilities")
    metadata: Dict[str, Any] = Field(..., description="Generation metadata")
```

**Error Responses**:
```json
// 400 Bad Request
{
  "detail": "Prompt cannot be empty"
}

// 422 Validation Error
{
  "detail": [
    {
      "loc": ["body", "temperature"],
      "msg": "ensure this value is less than or equal to 2.0",
      "type": "value_error.number.not_le"
    }
  ]
}

// 503 Service Unavailable
{
  "detail": "Model not loaded"
}
```

### Client Usage Examples

#### Python (httpx)
```python
import httpx
import asyncio

async def generate_tokens(prompt: str, temperature: float = 1.0):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/generate",
            json={
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": 1,
                "top_k": 5
            }
        )
        return response.json()

# Usage
result = asyncio.run(generate_tokens("The weather today is"))
print(result["tokens"])
```

#### JavaScript (fetch)
```javascript
async function generateTokens(prompt, temperature = 1.0) {
    const response = await fetch('http://localhost:8001/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            prompt: prompt,
            temperature: temperature,
            max_tokens: 1,
            top_k: 5
        })
    });
    
    return await response.json();
}

// Usage
generateTokens("The capital of France is")
    .then(result => console.log(result.tokens));
```

---

## Component Documentation

### Layout Components

#### `app_layout(content: rx.Component) -> rx.Component`
**Location**: `components/layout.py`

Main application layout providing consistent structure across all pages.

**Features**:
- Responsive three-column layout (sidebar, content, info panel)
- Consistent header with branding
- Navigation integration
- Mobile-responsive design

**Usage**:
```python
from ..components.layout import app_layout

@rx.page("/my-page")
def my_page():
    return app_layout(
        rx.vstack(
            rx.heading("My Page Content"),
            rx.text("Page content goes here..."),
            spacing="4"
        )
    )
```

### Color Coding System

#### `get_probability_color(probability: float) -> str`
**Location**: `components/color_coded_text.py`

Returns color for probability value using 6-tier gradient scale.

**Color Scale**:
- **80-100%**: `#10B981` (Green-500) - Very high probability
- **60-80%**: `#34D399` (Green-400) - High probability  
- **40-60%**: `#FCD34D` (Yellow-300) - Medium-high probability
- **20-40%**: `#F59E0B` (Amber-500) - Medium-low probability
- **10-20%**: `#F97316` (Orange-500) - Low probability
- **0-10%**: `#EF4444` (Red-500) - Very low probability

**Usage**:
```python
from ..components.color_coded_text import get_probability_color

color = get_probability_color(0.75)  # Returns "#34D399"
```

#### `probability_token_span_from_entry(entry, show_tooltip=True) -> rx.Component`
**Location**: `components/color_coded_text.py`

Creates color-coded span for token display with optional tooltip.

**Parameters**:
- `entry`: TokenHistoryEntry object (or Reflex Var)
- `show_tooltip`: Whether to show probability on hover
- `animate_on_hover`: Whether to add hover animations

**Usage**:
```python
# With Reflex foreach for dynamic lists
rx.foreach(
    TokenHistoryState.token_history,
    probability_token_span_from_entry
)
```

### Token Display Components

#### `token_pill(token: TokenProbability, is_selected=False) -> rx.Component`
**Location**: `components/probability_bar.py`

Creates clickable token pill with color-coded probability background.

**Features**:
- Color-coded background based on probability
- Selection state styling
- Hover effects
- Probability percentage display

**Usage**:
```python
from ..components.probability_bar import token_pill

# Static usage
token_pill(
    token=TokenProbability(token=" Paris", probability=0.82, percentage=82.0),
    is_selected=False
)

# Dynamic usage with event handler
rx.foreach(
    InteractiveGenerationState.current_alternatives,
    lambda token, index: token_pill(
        token=token,
        is_selected=InteractiveGenerationState.selected_token_index == index,
        on_click=InteractiveGenerationState.select_token(index)
    )
)
```

#### `interactive_probability_bars(alternatives: List[TokenProbability]) -> rx.Component`
**Location**: `components/probability_bar.py`

Main component for displaying token alternatives with probability bars and selection.

**Features**:
- Horizontal probability bars
- Click-to-select functionality
- Color-coded probabilities
- Responsive layout

### Visualization Components

#### Tree Visualization Components
**Location**: `utils/tree_structure.py`

**Classes**:
- `TreeNode`: Represents individual nodes in token tree
- `TokenTree`: Manages complete tree structure and operations
- Tree visualization uses Plotly for interactive graphs

**Key Methods**:
```python
class TokenTree:
    def add_node(self, parent_id: str, token: str, probability: float) -> str
    def expand_node(self, node_id: str, alternatives: List[TokenProbability]) -> None
    def get_path_to_root(self, node_id: str) -> List[TreeNode]
    def to_networkx(self) -> nx.DiGraph
```

---

## State Management

### State Architecture

Reflex uses a global state system with automatic WebSocket synchronization between frontend and backend.

#### Base State Pattern
```python
class MyState(rx.State):
    # State variables (automatically synchronized)
    my_data: str = ""
    is_loading: bool = False
    
    # Event handlers (can modify state)
    def update_data(self, new_value: str):
        self.my_data = new_value
    
    # Background events (for async operations)
    @rx.event(background=True)
    async def async_operation(self):
        async with self:  # Thread-safe state updates
            self.is_loading = True
        
        # Do async work...
        result = await some_async_function()
        
        async with self:
            self.my_data = result
            self.is_loading = False
```

### State Classes

#### `InteractiveGenerationState`
**Location**: `pages/interactive_mode.py`

Manages state for Mode 1 (Interactive Token Generation).

**Key State Variables**:
```python
class InteractiveGenerationState(rx.State):
    # Current session
    initial_prompt: str = ""
    current_text: str = ""
    generated_tokens: List[str] = []
    token_history: List[TokenHistoryEntry] = []
    
    # Current alternatives
    current_alternatives: List[TokenProbability] = []
    selected_token_index: int = -1
    
    # UI state
    is_generating: bool = False
    is_loading: bool = False
    has_started: bool = False
    
    # Configuration
    temperature: float = 1.0
    max_tokens: int = 10
```

**Key Methods**:
```python
async def start_generation(self, prompt: str):
    """Initialize generation with user prompt."""
    
async def generate_next_token(self):
    """Generate alternatives for next token."""
    
def select_token(self, index: int):
    """Select token and update state."""
    
def reset_generation(self):
    """Clear all generated content."""
```

#### `PromptComparisonState`
**Location**: `pages/prompt_comparison.py`

Manages state for Mode 2 (Prompt Comparison).

**Pattern**: Independent state for each of three columns:
```python
class PromptComparisonState(rx.State):
    # Column 1
    prompt_1: str = ""
    results_1: List[TokenProbability] = []
    is_loading_1: bool = False
    
    # Column 2
    prompt_2: str = ""
    results_2: List[TokenProbability] = []
    is_loading_2: bool = False
    
    # Column 3
    prompt_3: str = ""
    results_3: List[TokenProbability] = []
    is_loading_3: bool = False
```

#### `TokenTreeState`
**Location**: `pages/token_tree.py`

Manages state for Mode 3 (Token Tree Visualization).

**Key Features**:
```python
class TokenTreeState(rx.State):
    # Tree data
    tree: Optional[TokenTree] = None
    tree_figure: Optional[go.Figure] = None
    selected_node_id: Optional[str] = None
    
    # Generation state
    is_generating: bool = False
    is_expanding: bool = False
    
    # Point mapping for Plotly clicks
    point_to_node_mapping: List[str] = []
```

### State Best Practices

1. **Thread Safety**: Always use `async with self:` for background state updates
2. **Immutable Updates**: Replace collections instead of modifying in-place
3. **Error Handling**: Set error flags and messages in state
4. **Loading States**: Provide visual feedback for long operations
5. **Type Hints**: Use comprehensive type annotations

**Example - Thread-Safe Background Update**:
```python
@rx.event(background=True)
async def fetch_data(self):
    async with self:
        self.is_loading = True
        self.error_message = ""
    
    try:
        # Async operation outside state context
        result = await api_call()
        
        async with self:
            self.data = result
            self.has_data = True
    except Exception as e:
        async with self:
            self.error_message = str(e)
            self.has_error = True
    finally:
        async with self:
            self.is_loading = False
```

---

## Development Setup

### Environment Requirements

**Python Version**: 3.12+
**Package Manager**: UV (recommended) or pip
**Development Tools**: 
- Git
- Code editor with Python support
- Terminal/command line access

### Initial Setup

1. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd d-ai-token-visualizer
   ```

2. **Setup Virtual Environments**:
   ```bash
   # Main application
   cd token_visualizer
   uv venv
   uv sync
   
   # LLM service
   cd ../llm_service  
   uv venv
   uv sync
   ```

3. **Configure Environment**:
   ```bash
   # Copy example configs
   cp token_visualizer/.env.example token_visualizer/.env
   cp llm_service/.env.example llm_service/.env
   
   # Edit as needed
   ```

4. **Authenticate with Hugging Face**:
   ```bash
   huggingface-cli login
   ```

### Development Workflow

#### Running Services for Development

**Terminal 1 - LLM Service**:
```bash
cd llm_service
uv run uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - Main Application**:
```bash
cd token_visualizer
uv run reflex run
```

#### Code Style and Quality

**Formatting with Black**:
```bash
uv add black --dev
uv run black .
```

**Linting with Ruff**:
```bash
uv add ruff --dev
uv run ruff check .
uv run ruff check . --fix  # Auto-fix issues
```

**Type Checking with mypy**:
```bash
uv add mypy --dev
uv run mypy token_visualizer/ llm_service/
```

#### Pre-commit Hooks

```bash
# Install pre-commit
uv add pre-commit --dev

# Setup hooks
uv run pre-commit install

# Run manually
uv run pre-commit run --all-files
```

**`.pre-commit-config.yaml`**:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.254
    hooks:
      - id: ruff
        args: [--fix]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.1
    hooks:
      - id: mypy
```

### Adding New Features

#### New Component

1. **Create Component File**:
   ```bash
   touch token_visualizer/token_visualizer/components/my_component.py
   ```

2. **Component Template**:
   ```python
   """My new component for X functionality."""
   
   import reflex as rx
   from typing import Optional
   
   def my_component(
       prop1: str,
       prop2: Optional[int] = None,
       **kwargs
   ) -> rx.Component:
       """Create my custom component.
       
       Args:
           prop1: Description of prop1
           prop2: Optional description of prop2
           **kwargs: Additional props passed to container
           
       Returns:
           Reflex component
       """
       return rx.box(
           # Component content
           rx.text(prop1),
           # Use kwargs for styling
           **kwargs
       )
   ```

3. **Export Component**:
   ```python
   # In components/__init__.py
   from .my_component import my_component
   
   __all__ = ["my_component", ...]
   ```

#### New Page/Mode

1. **Create Page File**:
   ```bash
   touch token_visualizer/token_visualizer/pages/my_mode.py
   ```

2. **Page Template**:
   ```python
   """My new mode - Description of what it does."""
   
   import reflex as rx
   from ..components.layout import app_layout
   
   class MyModeState(rx.State):
       """State for my new mode."""
       
       # State variables
       user_input: str = ""
       is_loading: bool = False
       
       # Event handlers
       def handle_input(self, value: str):
           self.user_input = value
   
   def my_mode_content() -> rx.Component:
       """Main content for my mode."""
       return rx.vstack(
           rx.heading("My New Mode"),
           rx.text("Description of functionality"),
           # Mode-specific components
           spacing="4"
       )
   
   @rx.page("/my-mode", title="My Mode")
   def my_mode():
       """My mode page."""
       return app_layout(my_mode_content())
   ```

3. **Add Navigation**:
   ```python
   # In components/navigation.py
   rx.link(
       nav_button(
           icon="my-icon",
           label="My Mode"
       ),
       href="/my-mode",
       text_decoration="none",
       width="100%"
   )
   ```

#### New API Endpoint

1. **Add Endpoint to LLM Service**:
   ```python
   # In llm_service/main.py
   @app.post("/my-endpoint", response_model=MyResponse)
   async def my_endpoint(request: MyRequest):
       """My new API endpoint."""
       try:
           # Process request
           result = process_my_request(request)
           return MyResponse(data=result)
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))
   ```

2. **Add Client Method**:
   ```python
   # In token_visualizer/services/llm_client.py
   async def call_my_endpoint(self, data: MyRequest) -> MyResponse:
       """Call my new endpoint."""
       async with httpx.AsyncClient() as client:
           response = await client.post(
               f"{self.base_url}/my-endpoint",
               json=data.dict(),
               timeout=self.timeout
           )
           response.raise_for_status()
           return MyResponse(**response.json())
   ```

---

## Testing

### Testing Strategy

1. **Unit Tests**: Test individual functions and methods
2. **Integration Tests**: Test service communication  
3. **UI Tests**: Test component rendering and interactions
4. **End-to-End Tests**: Test complete user workflows

### Test Structure

```
tests/
├── unit/
│   ├── test_components.py
│   ├── test_state.py
│   └── test_utils.py
├── integration/
│   ├── test_llm_service.py
│   └── test_api_client.py
├── ui/
│   ├── test_interactive_mode.py
│   ├── test_prompt_comparison.py
│   └── test_token_tree.py
└── e2e/
    └── test_user_workflows.py
```

### Testing Setup

**Install Test Dependencies**:
```bash
uv add pytest pytest-asyncio httpx pytest-mock --dev
```

**Run Tests**:
```bash
# All tests
uv run pytest

# Specific test file
uv run pytest tests/unit/test_components.py

# With coverage
uv add pytest-cov --dev
uv run pytest --cov=token_visualizer --cov=llm_service
```

### Example Tests

**Unit Test Example**:
```python
# tests/unit/test_color_coding.py
import pytest
from token_visualizer.components.color_coded_text import get_probability_color

def test_probability_color_high():
    """Test color for high probability."""
    color = get_probability_color(0.85)
    assert color == "#10B981"  # Green-500

def test_probability_color_low():
    """Test color for low probability."""
    color = get_probability_color(0.05)
    assert color == "#EF4444"  # Red-500

@pytest.mark.parametrize("probability,expected", [
    (1.0, "#10B981"),
    (0.75, "#34D399"),
    (0.5, "#FCD34D"),
    (0.3, "#F59E0B"),
    (0.15, "#F97316"),
    (0.05, "#EF4444"),
])
def test_probability_color_ranges(probability, expected):
    """Test color ranges comprehensively."""
    assert get_probability_color(probability) == expected
```

**Integration Test Example**:
```python
# tests/integration/test_llm_service.py
import pytest
import httpx
from llm_service.schemas import GenerateRequest

@pytest.mark.asyncio
async def test_generate_endpoint():
    """Test LLM service generate endpoint."""
    async with httpx.AsyncClient(base_url="http://localhost:8001") as client:
        request = GenerateRequest(
            prompt="The capital of France is",
            temperature=1.0,
            max_tokens=1,
            top_k=5
        )
        
        response = await client.post("/generate", json=request.dict())
        
        assert response.status_code == 200
        data = response.json()
        
        assert "tokens" in data
        assert len(data["tokens"]) == 5
        assert all("token" in token for token in data["tokens"])
        assert all("probability" in token for token in data["tokens"])
```

**Mock Testing for LLM Service**:
```python
# tests/unit/test_state.py
import pytest
from unittest.mock import AsyncMock, patch
from token_visualizer.pages.interactive_mode import InteractiveGenerationState

@pytest.mark.asyncio
async def test_generate_next_token():
    """Test token generation with mocked LLM service."""
    state = InteractiveGenerationState()
    state.current_text = "The capital of France is"
    
    # Mock LLM service response
    mock_response = {
        "tokens": [
            {"token": " Paris", "probability": 0.8, "percentage": 80.0},
            {"token": " Lyon", "probability": 0.1, "percentage": 10.0},
        ]
    }
    
    with patch('token_visualizer.services.llm_client.get_llm_client') as mock_client:
        mock_client.return_value.generate.return_value = mock_response
        
        await state.generate_next_token()
        
        assert len(state.current_alternatives) == 2
        assert state.current_alternatives[0].token == " Paris"
        assert state.current_alternatives[0].probability == 0.8
```

### Performance Testing

**Load Testing LLM Service**:
```python
# tests/performance/test_load.py
import asyncio
import time
import httpx

async def test_concurrent_requests():
    """Test service under concurrent load."""
    async def make_request():
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8001/generate",
                json={
                    "prompt": "Test prompt",
                    "temperature": 1.0,
                    "max_tokens": 1,
                    "top_k": 5
                }
            )
            return response.status_code
    
    # Test 10 concurrent requests
    start_time = time.time()
    tasks = [make_request() for _ in range(10)]
    results = await asyncio.gather(*tasks)
    end_time = time.time()
    
    # All requests should succeed
    assert all(status == 200 for status in results)
    
    # Should complete within reasonable time
    assert end_time - start_time < 30.0  # 30 seconds max
```

---

## Contributing Guidelines

### Code Standards

1. **Python Style**: Follow PEP 8, use Black for formatting
2. **Type Hints**: Comprehensive type annotations required
3. **Docstrings**: Google-style docstrings for all public functions
4. **Error Handling**: Explicit error handling with user-friendly messages
5. **Comments**: Explain complex logic, avoid obvious comments

### Commit Guidelines

**Conventional Commits**:
```
type(scope): description

feat(ui): add new token selection component
fix(api): handle empty prompt error
docs(readme): update installation instructions
test(integration): add LLM service tests
refactor(state): simplify token history management
```

**Types**:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `style`: Code style changes
- `perf`: Performance improvements

### Pull Request Process

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make Changes**:
   - Write code following style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Changes**:
   ```bash
   # Run tests
   uv run pytest
   
   # Check code style
   uv run black --check .
   uv run ruff check .
   uv run mypy .
   ```

4. **Commit and Push**:
   ```bash
   git add .
   git commit -m "feat(ui): add new visualization mode"
   git push origin feature/my-new-feature
   ```

5. **Create Pull Request**:
   - Provide clear description of changes
   - Reference any related issues
   - Include screenshots for UI changes
   - Ensure all checks pass

### Issue Reporting

**Bug Reports Should Include**:
- Clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Python version, GPU/CPU)
- Error messages and logs
- Screenshots if applicable

**Feature Requests Should Include**:
- Clear description of desired functionality
- Use case or educational benefit
- Proposed implementation approach
- Potential impact on existing features

### Development Environment

**Recommended Tools**:
- **Editor**: VS Code with Python extension
- **Terminal**: Built-in terminal or external
- **Git**: Command line or GUI client
- **Debugging**: Python debugger integration

**VS Code Extensions**:
- Python (Microsoft)
- Pylance (Microsoft)
- Black Formatter
- Ruff
- Git Lens

**Development Configuration**:
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./token_visualizer/.venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

This completes the comprehensive developer documentation. The documentation covers architecture, APIs, components, state management, development setup, and contribution guidelines to help developers understand and contribute to the Token Visualizer project effectively.
