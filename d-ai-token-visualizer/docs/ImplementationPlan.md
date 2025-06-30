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
- [ ] Create `llm_service/` directory structure for separate FastAPI service
- [ ] Add FastAPI, Uvicorn dependencies to service requirements
- [ ] Create `llm_service/main.py` with basic FastAPI application
- [ ] Add `llm_service/config/settings.py` for service configuration
- [ ] Create Docker support files (`Dockerfile`, `.dockerignore`)
- [ ] Test basic FastAPI service runs on port 8001

### 3.2 Model Integration in Service
- [ ] Move existing local LLM code to `llm_service/models/gemma_model.py`
- [ ] Refactor model loading to happen once at service startup
- [ ] Add GPU/CPU device detection and memory management
- [ ] Implement model singleton pattern for efficient resource usage
- [ ] Add model health check and status endpoints
- [ ] Test model loading and memory usage in service

### 3.3 API Endpoints Implementation
- [ ] Create `llm_service/api/schemas.py` with Pydantic request/response models
- [ ] Implement `POST /generate` endpoint for token generation with probabilities
- [ ] Add `GET /health` endpoint for service health monitoring
- [ ] Add `GET /status` endpoint for model and service information
- [ ] Implement proper error handling and HTTP status codes
- [ ] Add request validation and response formatting
- [ ] Test all API endpoints with sample requests

### 3.4 Main App Service Client
- [ ] Remove direct model integration from main Reflex app
- [ ] Create `token_visualizer/services/llm_client.py` HTTP client
- [ ] Implement HTTP client with timeout, retry logic, and error handling
- [ ] Add service health monitoring and status checking
- [ ] Update configuration to include LLM service endpoint URL
- [ ] Test HTTP client connection and API calls

### 3.5 Configuration Test Page Update
- [ ] Update Configuration Test page to test LLM service connectivity
- [ ] Add service health status display (available/unavailable)
- [ ] Test service endpoints (`/health`, `/status`, `/generate`)
- [ ] Display model information retrieved from service
- [ ] Add service URL configuration and testing
- [ ] Implement graceful error handling for service unavailable scenarios
- [ ] Test end-to-end: service startup → main app connection → token generation

### 3.6 Service Integration Testing
- [ ] Create startup scripts for both services (LLM service + main app)
- [ ] Test service lifecycle: start LLM service first, then main app
- [ ] Verify service restart doesn't affect main app (graceful degradation)
- [ ] Test concurrent requests and service performance
- [ ] Add logging and monitoring for service communication
- [ ] Document service deployment and development workflow

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
- [ ] Test complete interactive flow end-to-end

### 5.5 Basic Error Handling
- [ ] Add error handling for API failures
- [ ] Implement user-friendly error messages
- [ ] Add loading states and progress indicators
- [ ] Test error scenarios and recovery
- [ ] Add timeout handling for long requests

## Phase 6: Enhanced Interactive Features

### 6.1 Token History and Navigation
- [ ] Add token history display
- [ ] Implement "Back" button to undo token selection
- [ ] Add "Reset" button to clear session
- [ ] Create token path visualization
- [ ] Test navigation and history management

### 6.2 Advanced Probability Display
- [ ] Add percentage display for each token
- [ ] Implement color-coded probability indicators
- [ ] Add hover tooltips with detailed information
- [ ] Create probability sorting options
- [ ] Test probability display accuracy

### 6.3 Configuration Options
- [ ] Add temperature control slider
- [ ] Implement max_tokens configuration
- [ ] Add top_logprobs count selector
- [ ] Create model selection dropdown
- [ ] Test configuration changes affect generation

## Phase 7: Mode 2 - Live Probability Visualization

### 7.1 Real-time Prompt Comparison
- [ ] Create `pages/live_probability.py` page
- [ ] Implement side-by-side prompt comparison
- [ ] Add debounced input handling
- [ ] Create real-time API call management
- [ ] Test live updates and performance

### 7.2 Probability Difference Visualization
- [ ] Implement before/after probability comparison
- [ ] Add visual indicators for probability changes
- [ ] Create difference highlighting
- [ ] Add statistical summaries
- [ ] Test comparison accuracy and performance

### 7.3 Prompt Templates
- [ ] Create library of educational prompt templates
- [ ] Implement template selection interface
- [ ] Add template customization options
- [ ] Create template management system
- [ ] Test template functionality and variety

## Phase 8: Mode 3 - Color-coded Visualization

### 8.1 Heat Map Implementation
- [ ] Create `pages/color_visualization.py` page
- [ ] Implement color mapping for probabilities
- [ ] Add gradient color scheme
- [ ] Create responsive heat map display
- [ ] Test color accuracy and accessibility

### 8.2 Interactive Hover Features
- [ ] Add detailed probability tooltips
- [ ] Implement token information display
- [ ] Create hover animations and transitions
- [ ] Add keyboard navigation support
- [ ] Test accessibility and usability

### 8.3 Visualization Export
- [ ] Implement export to PNG/SVG functionality
- [ ] Add export configuration options
- [ ] Create export button and handling
- [ ] Add export progress indicators
- [ ] Test export functionality and file quality

## Phase 9: Advanced Features and Polish

### 9.1 Performance Optimization
- [ ] Implement API response caching
- [ ] Add request batching where possible
- [ ] Optimize component re-rendering
- [ ] Add lazy loading for large datasets
- [ ] Performance test and benchmark

### 9.2 Accessibility Improvements
- [ ] Add ARIA labels and descriptions
- [ ] Implement keyboard navigation
- [ ] Add high contrast mode
- [ ] Test with screen readers
- [ ] Add color blind friendly options

### 9.3 Mobile Responsiveness
- [ ] Optimize mobile layouts
- [ ] Add touch-friendly controls
- [ ] Implement swipe gestures
- [ ] Test on various mobile devices
- [ ] Add progressive web app features

## Phase 10: Testing and Quality Assurance

### 10.1 Unit Testing
- [ ] Add `pytest` to dependencies
- [ ] Create unit tests for utility functions
- [ ] Test state management functions
- [ ] Add tests for API client
- [ ] Achieve minimum 80% code coverage

### 10.2 Integration Testing
- [ ] Create integration tests for API flows
- [ ] Test complete user workflows
- [ ] Add end-to-end testing with Playwright
- [ ] Test error scenarios and edge cases
- [ ] Verify performance under load

### 10.3 User Experience Testing
- [ ] Conduct usability testing sessions
- [ ] Gather feedback from target users
- [ ] Test educational effectiveness
- [ ] Identify and fix UX issues
- [ ] Validate learning objectives

## Phase 11: Documentation and Deployment Preparation

### 11.1 Documentation
- [ ] Create comprehensive README.md
- [ ] Add API documentation
- [ ] Create user guide and tutorials
- [ ] Add developer documentation
- [ ] Create troubleshooting guide

### 11.2 Docker Containerization
- [ ] Create Dockerfile for production
- [ ] Add docker-compose for local development
- [ ] Test container builds and runs
- [ ] Optimize container image size
- [ ] Add health check endpoints

### 11.3 Environment Configuration
- [ ] Create production environment configs
- [ ] Add environment variable validation
- [ ] Implement configuration management
- [ ] Add secrets management integration
- [ ] Test deployment configurations

## Phase 12: Production Deployment

### 12.1 Infrastructure as Code
- [ ] Create Terraform configuration
- [ ] Define Azure Container Apps setup
- [ ] Add networking and security configs
- [ ] Create environment-specific configs
- [ ] Test infrastructure deployment

### 12.2 CI/CD Pipeline
- [ ] Create GitHub Actions workflows
- [ ] Add automated testing pipeline
- [ ] Implement Docker image building
- [ ] Add security scanning
- [ ] Test complete deployment pipeline

### 12.3 Monitoring and Observability
- [ ] Add OpenTelemetry instrumentation
- [ ] Configure Azure Application Insights
- [ ] Set up custom metrics and alerts
- [ ] Create monitoring dashboards
- [ ] Test monitoring and alerting

## Phase 13: Production Validation

### 13.1 Deployment Testing
- [ ] Deploy to staging environment
- [ ] Run full test suite in staging
- [ ] Perform load testing
- [ ] Validate monitoring and logging
- [ ] Test disaster recovery procedures

### 13.2 Production Rollout
- [ ] Deploy to production environment
- [ ] Monitor initial production usage
- [ ] Validate performance metrics
- [ ] Collect user feedback
- [ ] Address any production issues

### 13.3 Post-Deployment
- [ ] Create operational runbooks
- [ ] Set up regular health checks
- [ ] Plan maintenance windows
- [ ] Create backup and recovery procedures
- [ ] Document lessons learned

## Verification Checklist for Each Phase

After completing each phase, verify:
- [ ] All features work as expected
- [ ] No new errors or warnings
- [ ] Performance is acceptable
- [ ] UI is responsive and accessible
- [ ] Documentation is updated
- [ ] Tests pass successfully
- [ ] Code is properly committed to git

## Success Criteria

The implementation is considered successful when:
- [ ] All three modes (Interactive, Live, Color-coded) work correctly
- [ ] Application handles Azure OpenAI API integration reliably
- [ ] UI is responsive and accessible
- [ ] Performance meets educational use requirements
- [ ] Deployment pipeline is functional
- [ ] Monitoring and observability are operational
- [ ] Documentation is comprehensive and accurate

## Notes

- Each phase should be completed and verified before moving to the next
- If any phase fails verification, address issues before proceeding
- Consider creating feature branches for each major phase
- Regular testing and feedback collection throughout development
- Keep design document updated as implementation progresses

## 🚨 CRITICAL ARCHITECTURE CHANGE - June 30, 2025

**Major Pivot: Azure OpenAI → Local Gemma 2 LLM**

Due to Azure OpenAI legacy completions API deprecation (affecting our core token-by-token generation functionality), we're switching to:

- **Model**: Google Gemma 2 2B base model (Hugging Face)
- **Benefits**: 
  - ✅ True text completion mode (no chat formatting)
  - ✅ Direct logits access (better than logprobs)
  - ✅ Local inference (no API limits/costs)
  - ✅ Future-proof (open source, no deprecation risk)
- **Impact**: All Phase 3 items updated to reflect local LLM integration
- **Test Script**: `test_local_llm.py` created to verify functionality
