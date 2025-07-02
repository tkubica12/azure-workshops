# Token Visualizer Implementation Plan

## Overview
This implementation plan provides a step-by-step checklist for building the Token Visualizer application using Reflex framework and Azure OpenAI. Each step is designed to be implementable and verifiable independently.

## Phase 1: Environment Setup & Project Initialization

### 1.1 Development Environment Setup
- [x] Install Python 3.11+ on development machine
- [x] Install `uv` package manager
- [x] Verify `uv` installation: `uv --version`
- [x] Create project directory: `d-ai-token-visualizer`
- [x] Initialize git repository
- [x] Create `.gitignore` file for Python/Reflex projects

### 1.2 Local LLM Setup
- [x] ~~Create Azure OpenAI resource in Azure portal~~ **REPLACED WITH LOCAL LLM**
- [x] Install PyTorch with CUDA support (if GPU available)
- [x] Install Hugging Face Transformers library
- [x] Download Gemma 2 2B base model from Hugging Face
- [x] Test local model loading and basic inference
- [x] Verify logits extraction functionality works with test request

### 1.3 Project Structure Creation
- [x] Create basic project structure following Reflex conventions
- [x] Create `pyproject.toml` with project metadata
- [x] Set up directory structure:
  ```
  token_visualizer/
  ├── token_visualizer/
  │   ├── __init__.py
  │   ├── pages/
  │   ├── components/
  │   ├── state/
  │   ├── services/
  │   └── utils/
  ├── assets/
  └── tests/
  ```

## Phase 2: Basic Reflex Application

### 2.1 Minimal Reflex App
- [x] Add Reflex to dependencies: `uv add reflex`
- [x] Create basic `rxconfig.py` configuration file
- [x] Create minimal app in `token_visualizer/__init__.py`
- [x] Create simple index page with "Hello World"
- [x] Test app runs locally: `reflex run`
- [x] Verify app opens in browser and displays correctly

### 2.2 Basic UI Structure
- [x] Create main layout component with header and content area
- [x] Add basic CSS styling and responsive design
- [x] Create navigation component (placeholder for future modes)
- [x] Add application title and basic branding
- [x] Test UI renders correctly on desktop and mobile

### 2.3 Environment Configuration
- [x] ~~Create `.env` file for environment variables~~ **SIMPLIFIED FOR LOCAL**
- [x] Add local model configuration variables (model path, device)
- [x] Implement configuration loading in application
- [x] Add model download and caching configuration
- [x] Test model loading and configuration works correctly

## Phase 3: Local LLM Service Development

### 3.1 Local LLM Service Setup
- [x] Create `llm_service/` directory structure for separate FastAPI service
- [x] Add FastAPI, Uvicorn dependencies to service pyproject.toml
- [x] Create `llm_service/main.py` with basic FastAPI application
- [x] Add `llm_service/config/settings.py` for service configuration
- [x] Create Docker support files (`Dockerfile`, `.dockerignore`)
- [x] Test basic FastAPI service runs on port 8001

### 3.2 Model Integration in Service
- [x] Move existing local LLM code to `llm_service/models/gemma_model.py`
- [x] Refactor model loading to happen once at service startup
- [x] Add GPU/CPU device detection and memory management
- [x] Implement model singleton pattern for efficient resource usage
- [x] Add model health check and status endpoints
- [x] Test model loading and memory usage in service

### 3.3 API Endpoints Implementation
- [x] Create `llm_service/api/schemas.py` with Pydantic request/response models
- [x] Implement `POST /generate` endpoint for token generation with probabilities
- [x] Add `GET /health` endpoint for service health monitoring
- [x] Add `GET /status` endpoint for model and service information
- [x] Implement proper error handling and HTTP status codes
- [x] Add request validation and response formatting
- [x] Test all API endpoints with sample requests

### 3.4 Main App Service Client
- [x] Remove direct model integration from main Reflex app
- [x] Create `token_visualizer/services/llm_client.py` HTTP client
- [x] Implement HTTP client with timeout, retry logic, and error handling
- [x] Add service health monitoring and status checking
- [x] Update configuration to include LLM service endpoint URL
- [x] Test HTTP client connection and API calls

### 3.5 Configuration Test Page Update
- [x] Update Configuration Test page to test LLM service connectivity
- [x] Add service health status display (available/unavailable)
- [x] Test service endpoints (`/health`, `/status`, `/generate`)
- [x] Display model information retrieved from service
- [x] Add service URL configuration and testing
- [x] Test end-to-end: service startup → main app connection → token generation

## Phase 4: Core State Management

### 4.1 Base State Classes
- [x] Create `state/base_state.py` with common functionality
- [x] Implement `state/token_state.py` for token data management
- [x] Add `state/ui_state.py` for UI state (loading, errors)
- [x] Create `state/settings_state.py` for app configuration
- [x] Test state management with simple counter example

### 4.2 Token State Implementation
- [x] Add properties for current prompt and token history
- [x] Implement methods to add/remove tokens
- [x] Add probability data management
- [x] Create methods for resetting and clearing state
- [x] Add state persistence for session management

### 4.3 State Integration Testing
- [x] Create test page to verify state updates
- [x] Test state persistence across page refreshes
- [x] Verify WebSocket updates work correctly
- [x] Test state with multiple concurrent users
- [x] Add debugging tools for state inspection

## Phase 5: Mode 1 - Interactive Token Generation (MVP)

### 5.1 Basic Token Display
- [x] Create `components/token_display.py` component
- [x] Implement clickable token buttons
- [x] Add basic styling for tokens
- [x] Display token text and probability
- [x] Test token selection and click events

### 5.2 Probability Visualization
- [x] Create `components/probability_bar.py` component
- [x] Implement horizontal probability bars
- [x] Add color coding for probability ranges
- [x] Create responsive design for different screen sizes
- [x] Test probability visualization with sample data

### 5.3 Prompt Input Interface
- [ ] ~~Create `components/prompt_input.py` component~~ **SKIPPED**
- [ ] ~~Implement multi-line text input~~ **SKIPPED**
- [ ] ~~Add real-time validation~~ **SKIPPED**
- [ ] ~~Create submit button and handling~~ **SKIPPED**
- [ ] ~~Test prompt input and submission~~ **SKIPPED**

**Note**: This phase is being skipped as the current probability visualization components provide sufficient functionality for the MVP. The prompt input interface can be implemented later if needed.

### 5.4 Interactive Generation Flow
- [x] Create `pages/interactive_mode.py` page
- [x] Integrate prompt input with token generation
- [x] Implement token selection and context building
- [x] Add "Next Token" generation cycle
- [x] Improve UI with temperature slider (0.0-2.0, 0.1 steps)
- [x] Add max tokens slider (1-100, 1 step)
- [x] Fix compilation errors with sliders
- [x] Implement interactive slider functionality (event handlers)
- [x] Test complete interactive flow end-to-end

### 5.5 Basic Error Handling
- [x] Add error handling for API failures
- [x] Implement user-friendly error messages
- [x] Add loading states and progress indicators
- [x] Add timeout handling for long requests

## Phase 6: Enhanced Interactive Features

### 6.1 Token History and Navigation
- [x] Add "Reset" button to clear session

### 6.2 Advanced Probability Display
- [x] Implement color-coded background for tokens added to Generate Text field
- [x] Add hover tooltips with detailed information when mouse goes over current prompt showing percentage probability of tokens added
- [x] Decide colored scale for probabilities with highly probable being green, low probability being red and others in between (amber, yellow and so on)

### 6.3 Configuration Options
- [x] Add temperature control slider

### 6.4 Complete 20 more
- [x] Add button that would ask API for 20 next token sampled with temperature and display probabilities of next (21st) token

## Phase 7: Mode 2 - Prompt Comparison Mode (Simplified) - COMPLETED ✅

### 7.1 Fixed Three-Column UI - COMPLETED ✅
- [x] Create `pages/prompt_comparison.py` page with fixed three-column layout
- [x] Design a simple `PromptColumn` component with:
  - Text area for prompt input
  - "Generate" button 
  - Token probability visualization area
- [x] Implement CSS Grid or Flexbox layout for three equal-width columns
- [x] Add navigation menu item for "Prompt Comparison" mode
- [x] Test basic three-column layout renders correctly

### 7.2 State Management and Generation - COMPLETED ✅
- [x] Create `PromptComparisonState` with three independent prompt-result pairs
- [x] Add state variables: `prompt_1`, `prompt_2`, `prompt_3` and corresponding `results_1`, `results_2`, `results_3`
- [x] Implement generate button handlers for each column (fixed temperature=1.0)
- [x] Reuse existing LLM service client for API calls
- [x] Add loading states for each column independently
- [x] Test state management and API integration for all three columns

### 7.3 Probability Visualization - COMPLETED ✅
- [x] Reuse existing color-coded probability components from Mode 1
- [x] Display top 5 token probabilities in each column using established 6-tier color system
- [x] Ensure consistent styling across all three columns
- [x] Add basic error handling for failed generations
- [x] Test complete workflow: prompt input → generate → probability display

## Phase 8: Mode 3 - Interactive Token Tree with Color Visualization

**ARCHITECTURAL DECISION - Plotly vs SVG**: 
Based on development analysis, we've chosen **Plotly with NetworkX** over custom SVG rendering for the following reasons:
- ✅ **Native Reflex Integration**: `rx.plotly` component provides seamless integration
- ✅ **Professional Layouts**: NetworkX algorithms handle tree positioning automatically
- ✅ **Interactive by Default**: Zoom, pan, hover, and click events built-in
- ✅ **Zero Custom Code**: No need for manual SVG rendering or layout calculations
- ✅ **Performance**: Optimized for large datasets and complex visualizations
- ✅ **Maintenance**: Well-established libraries with active community support
- ✅ **Educational Value**: Professional-grade visualization enhances learning experience

**CURRENT STATUS (Phase 8.2 - Tree Visualization Components)**:
- ✅ **Dependencies**: Plotly and NetworkX successfully added to project
- ✅ **Test Page**: Created `tree_visualization_test.py` with Plotly integration
- ✅ **State Management**: Implemented Plotly Figure state variables with reactive updates
- ✅ **Sample Tree**: Created sample tree data generation for testing
- ✅ **Basic Rendering**: Plotly tree visualization displaying with NetworkX layout
- ⚠️ **In Progress**: Fine-tuning interactive features and node styling
- 📝 **Next**: Complete tree controls integration and LLM service connection

**Key Technical Achievements**:
- Successfully integrated `rx.plotly` component with Reflex state management
- Implemented NetworkX tree layout algorithms for automatic node positioning
- Created reactive Plotly figure updates through event handlers
- Established color-coded node visualization using probability-based styling
- Added interactive zoom, pan, and hover functionality through Plotly's built-in features

### 8.1 Tree Data Structure and State Management - COMPLETED ✅
- [x] Create `utils/tree_structure.py` with token tree data model
- [x] Implement `TreeNode` class to represent branching points
- [x] Add tree state management in `state/tree_state.py`
- [x] Create methods for adding branches, navigating tree, and resetting
- [x] Test tree data structure with sample branching scenarios

### 8.2 Tree Visualization Components - IN PROGRESS ⚠️
- [x] Add Plotly and NetworkX dependencies for professional tree visualization
- [x] Create `components/token_tree.py` for Plotly-based tree rendering
- [ ] Implement NetworkX-based tree layout with automatic node positioning
- [x] Add color-coded token visualization using existing 6-tier color system
- [ ] Create responsive tree layout using Plotly's built-in responsive features
- [x] Add zoom and pan functionality through Plotly's native interaction controls
- [x] Integrate Plotly Figure state management with Reflex state system
- [ ] Test interactive tree visualization with sample data

### 8.3 Interactive Tree Page Implementation
- [x] Create `pages/tree_visualization_test.py` test page with Plotly tree interface
- [ ] Create `pages/token_tree.py` as mode 3 page with navigation MODES in left navigation bar
- [ ] Create simple input text for user to enter prompt and Generate button
- [ ] Create UI element to configure tree depth and branching factor - this will be reflected in subsequent calls to LLM service
- [x] Implement sample tree data generation and Plotly figure creation
- [x] Add Plotly-based tree rendering with NetworkX layout algorithms
- [x] Create tree controls for depth and branching configuration
- [x] Add interactive features through Plotly's built-in event system
- [ ] Test complete tree building and branching workflow with LLM integration
- [ ] Implement path selection and continuation for configurable depth (1-20 tokens)
- [ ] Create branching functionality - clicking nodes to create new paths
- [ ] Add tree management controls (reset, clear branches, configure depth)

### 8.4 Advanced Tree Features
- [ ] Implement hover tooltips with token information through Plotly's hover system
- [ ] Add visual path distinction using Plotly edge and node styling
- [ ] Create branch management through Plotly figure updates
- [ ] Add probability-weighted visual styling (node size, edge thickness based on probabilities)
- [ ] Implement tree export functionality using Plotly's built-in export features (PNG/SVG/HTML)
- [ ] Add keyboard navigation integration with Plotly events

### 8.5 Tree Performance and Optimization
- [ ] Leverage Plotly's optimized rendering for large trees (built-in virtualization)
- [ ] Implement efficient tree traversal using NetworkX algorithms
- [ ] Add lazy loading for deep tree branches through Plotly figure updates
- [ ] Utilize NetworkX graph pruning functionality to manage memory usage
- [ ] Test performance with complex trees using Plotly's performance monitoring (10+ levels, 5+ branches per level)

## Phase 9: Core Features Polish and Optimization

### 9.1 Performance Optimization
- [ ] Implement API response caching for repeated requests
- [ ] Optimize component re-rendering across all modes
- [ ] Add request debouncing for interactive elements
- [ ] Leverage Plotly's built-in performance features for complex tree structures
- [ ] Utilize NetworkX algorithms for efficient graph operations and memory optimization

### 9.2 Cross-Mode Consistency
- [ ] Ensure consistent color coding across all modes
- [ ] Standardize UI patterns and interactions
- [ ] Create shared component library for common elements
- [ ] Test seamless navigation between modes
- [ ] Validate consistent user experience

## Phase 10: Essential Documentation

### 10.1 User Documentation
- [ ] Create comprehensive README.md with setup instructions
- [ ] Add user guide for each mode with screenshots
- [ ] Create educational content explaining LLM concepts
- [ ] Add troubleshooting guide for common issues
- [ ] Document configuration options and settings

### 10.2 Developer Documentation
- [ ] Add API documentation for LLM service
- [ ] Create component documentation
- [ ] Document state management patterns
- [ ] Add contribution guidelines
- [ ] Create development setup guide

## Phase 11: Container Deployment

### 11.1 Docker Containerization
- [ ] Create Dockerfile for main Reflex application
- [ ] Create Dockerfile for LLM service
- [ ] Add docker-compose.yml for local development
- [ ] Optimize container image sizes
- [ ] Add health check endpoints for containers

### 11.2 Production Configuration
- [ ] Create production environment configs
- [ ] Add environment variable validation
- [ ] Implement proper logging and monitoring
- [ ] Add container security best practices
- [ ] Test complete containerized deployment

### 11.3 Deployment Documentation
- [ ] Create deployment guide for containers
- [ ] Add cloud deployment options (Azure Container Apps, etc.)
- [ ] Create infrastructure documentation
- [ ] Add scaling and monitoring guidelines
- [ ] Document backup and recovery procedures

