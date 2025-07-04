# Contributing Guidelines

## Welcome

Thank you for your interest in contributing to the Token Visualizer project! This guide will help you understand how to contribute effectively, whether you're fixing bugs, adding features, improving documentation, or enhancing the educational content.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Contribution Types](#contribution-types)
5. [Development Workflow](#development-workflow)
6. [Code Standards](#code-standards)
7. [Testing Guidelines](#testing-guidelines)
8. [Documentation Standards](#documentation-standards)
9. [Pull Request Process](#pull-request-process)
10. [Issue Reporting](#issue-reporting)

---

## Code of Conduct

### Our Pledge
We are committed to providing a friendly, safe, and welcoming environment for all contributors, regardless of experience level, gender identity, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, religion, or nationality.

### Expected Behavior
- Be respectful and inclusive in all interactions
- Welcome newcomers and help them get started
- Focus on constructive feedback and collaboration
- Respect different viewpoints and experiences
- Show empathy towards other community members

### Unacceptable Behavior
- Harassment, discrimination, or intimidation
- Offensive comments or personal attacks
- Trolling or deliberately disruptive behavior
- Spam or off-topic discussions
- Sharing private information without consent

### Reporting Issues
If you experience or witness unacceptable behavior, please report it to the project maintainers. All reports will be handled confidentially.

---

## Getting Started

### Prerequisites
- **Python 3.12+** installed on your system
- **Git** for version control
- **Basic understanding** of Python and web development
- **Familiarity** with machine learning concepts (helpful but not required)

### Project Overview
The Token Visualizer is an educational application with two main components:
1. **Main Application**: Reflex-based web interface
2. **LLM Service**: FastAPI service for model inference

### Educational Focus
This project is designed for **educational purposes**. All contributions should consider:
- **Learning outcomes**: How does this help students understand LLMs?
- **Accessibility**: Can beginners understand and use this feature?
- **Clarity**: Are concepts explained clearly and intuitively?

---

## Development Setup

### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/token-visualizer.git
cd token-visualizer

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL-OWNER/token-visualizer.git
```

### 2. Set Up Development Environment
```bash
# Install UV package manager (recommended)
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Install Dependencies
```bash
# Main application
cd token_visualizer
uv sync

# LLM service
cd ../llm_service
uv sync

# Return to project root
cd ..
```

### 4. Configure Environment
```bash
# Copy example configurations
cp token_visualizer/.env.example token_visualizer/.env
cp llm_service/.env.example llm_service/.env

# Edit configurations as needed
# For development, the defaults usually work fine
```

### 5. Verify Setup
```bash
# Terminal 1: Start LLM service
cd llm_service
uv run uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2: Start main application
cd token_visualizer
uv run reflex run

# Visit http://localhost:3000 to verify everything works
```

---

## Contribution Types

### 🐛 Bug Fixes
- Fix functional issues or incorrect behavior
- Improve error handling and user experience
- Resolve performance problems

**Examples**:
- Fix token display rendering issues
- Correct probability calculations
- Improve error messages

### ✨ New Features
- Add new educational modes or visualizations
- Implement new UI components
- Enhance existing functionality

**Examples**:
- New visualization types
- Additional model support
- Enhanced user interface elements

### 📚 Educational Content
- Improve explanations of LLM concepts
- Add educational exercises or examples
- Create learning materials

**Examples**:
- Better onboarding tutorials
- Concept explanations
- Example prompts and use cases

### 🔧 Technical Improvements
- Code refactoring and optimization
- Performance improvements
- Infrastructure enhancements

**Examples**:
- Code organization improvements
- API optimization
- Testing infrastructure

### 📖 Documentation
- API documentation improvements
- User guide enhancements
- Developer documentation

**Examples**:
- Tutorial improvements
- API reference updates
- Installation guide clarifications

---

## Development Workflow

### 1. Choose an Issue
- Browse [open issues](https://github.com/project/issues)
- Look for issues labeled `good first issue` for beginners
- Comment on issues you'd like to work on

### 2. Create a Branch
```bash
# Update your fork
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### 3. Make Changes
- Write clean, well-documented code
- Follow the project's coding standards
- Add tests for new functionality
- Update documentation as needed

### 4. Test Your Changes
```bash
# Run tests
uv run pytest

# Check code style
uv run black --check .
uv run ruff check .

# Test manually
# Start both services and verify functionality
```

### 5. Commit Changes
```bash
# Add changes
git add .

# Commit with descriptive message
git commit -m "feat: add new token visualization component"

# Push to your fork
git push origin feature/your-feature-name
```

### 6. Create Pull Request
- Go to GitHub and create a pull request
- Fill out the pull request template
- Link to relevant issues
- Request review from maintainers

---

## Code Standards

### Python Style Guide
We follow **PEP 8** with some project-specific conventions:

#### Formatting
- Use **Black** for code formatting
- Line length: 88 characters (Black default)
- Use **double quotes** for strings
- Use **trailing commas** in multi-line collections

#### Code Organization
```python
# Standard library imports
import os
import sys
from typing import List, Optional

# Third-party imports
import reflex as rx
import httpx

# Local imports
from ..components.layout import app_layout
from ..services.llm_client import get_llm_client
```

#### Naming Conventions
- **Classes**: `PascalCase` (e.g., `TokenGenerationState`)
- **Functions/Methods**: `snake_case` (e.g., `generate_next_token`)
- **Variables**: `snake_case` (e.g., `current_alternatives`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_TOKENS`)
- **Private members**: `_leading_underscore` (e.g., `_internal_method`)

### Type Hints
Use comprehensive type hints:
```python
from typing import List, Optional, Dict, Any, Union

def process_tokens(
    tokens: List[str],
    probabilities: Dict[str, float],
    threshold: Optional[float] = None
) -> List[TokenProbability]:
    """Process tokens with probability information."""
    # Implementation
```

### Documentation
Use **Google-style docstrings**:
```python
def calculate_probability(logits: List[float], temperature: float = 1.0) -> List[float]:
    """Calculate probabilities from logits using temperature scaling.
    
    Args:
        logits: Raw logit values from the model
        temperature: Temperature for scaling (0.0-2.0)
        
    Returns:
        List of probability values that sum to 1.0
        
    Raises:
        ValueError: If temperature is not in valid range
        
    Example:
        >>> logits = [1.0, 2.0, 0.5]
        >>> probs = calculate_probability(logits, temperature=1.0)
        >>> sum(probs)  # Should be close to 1.0
        1.0
    """
```

### Error Handling
- Use specific exception types
- Provide helpful error messages
- Log errors appropriately
- Handle edge cases gracefully

```python
def load_model(model_name: str) -> Model:
    """Load a model with proper error handling."""
    try:
        model = AutoModelForCausalLM.from_pretrained(model_name)
        return model
    except OSError as e:
        raise ModelNotFoundError(f"Model '{model_name}' not found: {e}")
    except Exception as e:
        raise ModelLoadError(f"Failed to load model '{model_name}': {e}")
```

### Reflex-Specific Guidelines

#### Component Props
- **Always use string literals** for Reflex props:
  ```python
  # ✅ Correct
  rx.vstack(..., spacing="4")
  rx.button(..., size="3")
  
  # ❌ Wrong
  rx.vstack(..., spacing="1rem")
  rx.button(..., size="lg")
  ```

#### State Management
- Use type hints for state variables
- Implement proper event handlers
- Use background events for async operations

```python
class MyState(rx.State):
    """Example state class."""
    
    # State variables with types
    current_text: str = ""
    is_loading: bool = False
    items: List[str] = []
    
    # Event handlers
    def update_text(self, text: str):
        """Update current text."""
        self.current_text = text
    
    # Background events for async operations
    @rx.event(background=True)
    async def fetch_data(self):
        """Fetch data asynchronously."""
        async with self:
            self.is_loading = True
        
        try:
            # Async operation
            data = await fetch_remote_data()
            
            async with self:
                self.items = data
        except Exception as e:
            async with self:
                self.error_message = str(e)
        finally:
            async with self:
                self.is_loading = False
```

---

## Testing Guidelines

### Test Structure
```
tests/
├── unit/           # Unit tests for individual functions
├── integration/    # Tests for component interaction
├── ui/            # UI component tests
└── e2e/           # End-to-end workflow tests
```

### Writing Tests
Use **pytest** with appropriate fixtures:
```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def sample_tokens():
    """Sample token data for testing."""
    return [
        {"token": " Paris", "probability": 0.8, "percentage": 80.0},
        {"token": " London", "probability": 0.2, "percentage": 20.0},
    ]

def test_probability_calculation(sample_tokens):
    """Test probability calculation logic."""
    result = calculate_probabilities(sample_tokens)
    assert abs(sum(result) - 1.0) < 0.001

@pytest.mark.asyncio
async def test_async_generation():
    """Test async token generation."""
    with patch('services.llm_client.generate') as mock_generate:
        mock_generate.return_value = {"tokens": sample_tokens}
        
        result = await generate_next_token("test prompt")
        assert len(result) == 2
```

### Test Coverage
- Aim for **80%+ code coverage**
- Focus on critical paths and edge cases
- Test both success and failure scenarios
- Include integration tests for API interactions

### Running Tests
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/unit/test_components.py

# Run with coverage
uv run pytest --cov=token_visualizer --cov=llm_service

# Run only fast tests (exclude slow integration tests)
uv run pytest -m "not slow"
```

---

## Documentation Standards

### README Updates
- Keep installation instructions current
- Update feature descriptions
- Add new configuration options
- Include relevant screenshots

### Code Documentation
- Document all public functions and classes
- Include usage examples
- Explain complex algorithms
- Document configuration options

### API Documentation
- Keep OpenAPI specs updated
- Include request/response examples
- Document error codes and handling
- Provide client code examples

### Educational Content
- Explain concepts clearly for beginners
- Provide step-by-step tutorials
- Include practical examples
- Link to relevant educational resources

---

## Pull Request Process

### Before Creating a PR

1. **Update your branch**:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-feature-branch
   git merge main
   ```

2. **Run quality checks**:
   ```bash
   uv run black .
   uv run ruff check . --fix
   uv run pytest
   ```

3. **Update documentation** if needed

### PR Description Template
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Educational content
- [ ] Documentation update
- [ ] Code refactoring

## Testing
- [ ] All tests pass
- [ ] Added tests for new functionality
- [ ] Manual testing completed

## Educational Impact
How does this change improve the educational value?

## Screenshots (if applicable)
Include screenshots for UI changes.

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or clearly documented)
```

### Review Process
1. **Automated checks** must pass
2. **Maintainer review** required
3. **Educational review** for content changes
4. **Final approval** from project lead

### After Approval
- **Squash and merge** preferred for clean history
- **Delete feature branch** after merge
- **Update local repository**:
  ```bash
  git checkout main
  git pull upstream main
  git branch -d your-feature-branch
  ```

---

## Issue Reporting

### Bug Reports
Use the bug report template:
```markdown
## Bug Description
Clear description of the bug.

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Environment
- OS: [e.g., Windows 11, macOS 13, Ubuntu 22.04]
- Python version: [e.g., 3.12.0]
- Browser: [e.g., Chrome 118, Firefox 119]
- GPU: [e.g., RTX 4090, M2 Pro, CPU only]

## Screenshots
Include screenshots if applicable.

## Additional Context
Any other relevant information.
```

### Feature Requests
Use the feature request template:
```markdown
## Feature Description
Clear description of the requested feature.

## Educational Value
How would this improve learning about LLMs?

## Use Case
Specific scenario where this would be helpful.

## Proposed Implementation
Ideas for how this could be implemented.

## Alternatives Considered
Other approaches you've considered.

## Additional Context
Any other relevant information.
```

### Question / Discussion
For questions or discussions:
```markdown
## Question
Your question about the project.

## Context
Background information or what you're trying to accomplish.

## What You've Tried
Steps you've already taken to find the answer.
```

---

## Community Guidelines

### Communication
- **Be respectful** in all interactions
- **Ask questions** if you're unsure about anything
- **Share knowledge** and help other contributors
- **Provide constructive feedback** in reviews

### Getting Help
- **Check existing issues** and documentation first
- **Search closed issues** for similar problems
- **Ask in discussions** for general questions
- **Tag maintainers** for urgent issues

### Recognition
Contributors are recognized through:
- **Commit attribution** in git history
- **Contributors list** in README
- **Release notes** for significant contributions
- **Special recognition** for educational content

---

## Development Tips

### Local Development
- **Use hot reload** for faster iteration
- **Test on different devices** for responsive design
- **Monitor performance** with different models
- **Check browser console** for JavaScript errors

### Debugging
- **Use browser dev tools** for UI issues
- **Check service logs** for API problems
- **Use Python debugger** for complex logic
- **Test edge cases** thoroughly

### Performance
- **Profile code** for bottlenecks
- **Optimize API calls** to reduce latency
- **Test with different hardware** configurations
- **Monitor memory usage** during development

---

## Resources

### Learning Materials
- **Reflex Documentation**: https://reflex.dev/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Hugging Face Transformers**: https://huggingface.co/docs/transformers
- **Machine Learning Concepts**: Various online courses

### Tools and Extensions
- **VS Code Python Extension**: Enhanced Python development
- **Black Formatter**: Code formatting
- **Ruff Linter**: Fast Python linter
- **Pytest**: Testing framework

### Community
- **GitHub Discussions**: Project discussions
- **Issues**: Bug reports and feature requests
- **Pull Requests**: Code contributions
- **Discord/Slack**: Real-time communication (if available)

---

## Questions?

If you have questions about contributing, please:
1. Check the existing documentation
2. Search through issues and discussions
3. Create a new discussion with your question
4. Tag relevant maintainers for attention

Thank you for contributing to the Token Visualizer project! Your contributions help make machine learning education more accessible and engaging for everyone.
