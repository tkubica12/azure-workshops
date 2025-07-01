# Token Visualizer Design Document

## Overview

The Token Visualizer is an educational application designed to help students understand autoregressive Large Language Models (LLMs) from the perspective of next token prediction. The application provides interactive visualization of token generation probabilities using Azure OpenAI service with logprobs functionality.

## Objectives

- **Educational Focus**: Help students understand how LLMs work at the token level
- **Interactive Learning**: Provide hands-on experience with token selection and probability visualization
- **Real-time Feedback**: Show how prompt modifications affect token probabilities
- **Visual Understanding**: Use colors, probabilities, and interactive elements to make abstract concepts concrete

## Architecture Overview

### Main Application (Reflex Frontend + Backend)
- **Technology**: Python with Reflex Framework
- **Architecture**: Full-stack Python development with React/Next.js under the hood
- **Interface**: Web-based interactive UI with modern components
- **Real-time Updates**: Built-in WebSocket communication between frontend and backend
- **Backend**: Reflex's built-in FastAPI backend for UI state management and API coordination

### Local LLM Service (Separate Microservice)
- **Technology**: Python with FastAPI
- **Model**: Google Gemma 2 2B base model via Hugging Face
- **ML Framework**: Hugging Face Transformers
- **Inference**: Local GPU/CPU inference (PyTorch)
- **Hardware**: Local GPU (CUDA) or CPU fallback
- **Deployment**: Separate service with independent lifecycle
- **API**: REST API for token generation and probability extraction
- **Port**: Default port 8001 (configurable)

**CRITICAL - Reflex Component Props:**
- **Spacing Values**: MUST use string literals `"0"` to `"9"` (NOT CSS values like `"1rem"`)
- **Size Values**: MUST use string literals `"1"` to `"9"` (NOT CSS values)
- **Prop Validation**: Reflex enforces strict prop types - always check existing working code
- **Common Error**: `TypeError: Invalid var passed for prop VStack.spacing` indicates wrong prop type

### Service Integration
- **Communication**: HTTP REST API calls from Reflex app to Local LLM service
- **Endpoint**: Configurable LLM service endpoint (e.g., `http://localhost:8001`)
- **Authentication**: Optional API key for service-to-service communication
- **Health Checks**: Service availability monitoring and error handling
- **Fallback**: Graceful degradation when LLM service is unavailable

## Core Features & Modes

### Mode 1: Interactive Token-by-Token Generation

**Description**: The primary mode where users experience step-by-step token generation with choice selection.

**User Flow**:
1. User enters an initial prompt
2. System calls Local LLM Service API with prompt to get top 5 token alternatives
3. Display shows:
   - Current prompt/context
   - 5 possible next tokens with their probabilities
   - Visual probability bars or percentages
4. User selects one token (mouse click or keyboard)
5. Selected token is appended to context
6. Process repeats for next token

**Advanced Features**:
- **Look-ahead Prediction**: Pre-calculate one token ahead for each of the 5 options
- **Probability Visualization**: Color-coded probability bars
- **Token Highlighting**: Visual distinction between user-selected and top-probability tokens
- **History Tracking**: Ability to backtrack and try different token paths

**Technical Requirements**:
- HTTP API call management to Local LLM Service
- Reflex state management for current context and token history
- Reactive UI components for token selection
- Background task handling for API calls
- Service availability monitoring and error handling

### Mode 2: Live Probability Visualization

**Description**: An analytical mode for real-time visualization of how prompt modifications affect next-token probabilities. It allows users to compare multiple prompt variations side-by-side to understand the impact of their inputs.

**User Flow**:
1.  User enters a base prompt in the first column (e.g., "The capital of France is").
2.  The system generates and displays the top 5 next-token probabilities for that prompt.
3.  The user can then create a new, modified prompt in a second column (e.g., adding a system message: "You are a helpful assistant. The capital of France is").
4.  The system generates probabilities for the second prompt, displaying them next to the first for immediate comparison.
5.  Users can continue adding columns for more prompt variations, creating a historical and comparative view.

**UI Design Concept**:
-   **Multi-Column Layout**: The interface will feature a dynamically expanding multi-column layout. Each column represents a distinct prompt and its resulting token probabilities.
-   **Prompt History**: Each column clearly displays the full prompt used for generation.
-   **Side-by-Side Comparison**: Token probabilities for each prompt are displayed in parallel, making it easy to spot differences.
-   **Probability Difference Highlighting**: The UI will visually highlight changes in probabilities for the same token across different prompts (e.g., an arrow up/down with the percentage change).
-   **Consistent Color Coding**: The established 6-tier color system will be used for probability values, ensuring visual consistency with other modes.
-   **Independent Configuration**: Each column will have its own temperature and configuration settings, allowing for isolated experiments.

**Features**:
-   **Side-by-side Prompt Comparison**: Compare an unlimited number of prompt variations.
-   **Probability Difference Highlighting**: Show increases/decreases in token probabilities.
-   **Real-time Updates**: Debounced API calls provide near real-time feedback as the user types.
-   **Prompt Templates**: Pre-defined prompt modifications for common educational scenarios.
-   **State Management**: Each column's state (prompt, results, settings) is managed independently.

**Technical Requirements**:
-   Dynamic UI component for adding/removing prompt columns.
-   Debounced API calls to the Local LLM Service for each column's prompt.
-   Efficient diff calculation and UI updates for probability changes.
-   Horizontal scrolling or adaptive layout to manage multiple columns.
-   State management capable of handling a list of independent prompt-result objects.

### Mode 3: Interactive Token Tree with Color Visualization

**Description**: Advanced visualization combining color-coded probabilities with interactive branching paths, allowing users to explore multiple token generation possibilities in a tree structure.

**Core Concept**:
The mode leverages existing token probability functionality to create an interactive tree where users can explore different generation paths. Starting with an initial prompt, the system shows the top 5 possible next tokens as branches, then allows users to select a path and continue for a configurable number of tokens (e.g., 10). Users can then click on any unselected token at any branching point to create alternative paths, building a comprehensive tree of possibilities.

**User Flow**:
1. **Initial Generation**: User enters prompt, system generates top 5 token probabilities
2. **Path Selection**: User selects one token, system continues generation for configured depth (e.g., 10 tokens)
3. **Tree Display**: Full path is shown with all possible branches at each step (selected and unselected)
4. **Interactive Branching**: User can click any unselected token at any point to branch from there
5. **Multiple Paths**: Previous branches remain visible, creating a growing tree visualization
6. **Exploration**: Users can create multiple branches to compare different generation paths

**Features**:
- **Color-coded Probabilities**: Tokens colored by probability using the established 6-tier system
  - Very High (80-100%): Green shades
  - High (60-80%): Light green  
  - Medium-High (40-60%): Yellow
  - Medium (20-40%): Orange
  - Low (10-20%): Light red
  - Very Low (0-10%): Red shades
- **Interactive Tree Structure**: Clickable nodes for branching at any point
- **Visual Path Distinction**: Different visual styles for selected vs. unselected paths
- **Probability-weighted Styling**: Branch thickness or opacity based on token probability
- **Hover Information**: Detailed probability and token information on hover
- **Configurable Depth**: User can set how many tokens to generate per path (1-20)
- **Tree Management**: Ability to clear branches, reset tree, or focus on specific subtrees

**Technical Requirements**:
- **Tree Data Structure**: Efficient representation of branching token sequences
- **State Management**: Track multiple paths and branching points
- **Visual Rendering**: SVG or Canvas-based tree visualization
- **Interactive Events**: Click handling for branching actions
- **Performance**: Efficient rendering for complex trees with many branches
- **Memory Management**: Handle large trees without performance degradation

**Educational Benefits**:
- **Path Comparison**: Students can see how different token choices lead to different outcomes
- **Probability Understanding**: Visual representation of why certain paths are more likely
- **Decision Point Awareness**: Understanding that each token choice affects all future possibilities
- **Alternative Exploration**: Easy exploration of "what if" scenarios at any point

## Technical Specifications

### Local LLM Service Architecture

**Service Deployment**:
```
Technology: FastAPI with Python 3.11+
Model: google/gemma-2-2b (base model)
Framework: Hugging Face Transformers
Hardware: Local GPU (CUDA preferred) or CPU
Memory: ~5GB GPU VRAM or 8GB+ system RAM
Port: 8001 (configurable)
Lifecycle: Independent of main Reflex application
```

**API Endpoints**:
```
GET  /health                    - Service health check (root level)
GET  /api/v1/status             - Model loading status and info
POST /api/v1/generate           - Token generation with probabilities
POST /api/v1/test               - Simple test generation endpoint
```

**Model Configuration**:
```
Parameters:
  - max_new_tokens: configurable (default: 1)
  - temperature: configurable (default: 0.7)
  - top_k: configurable (default: 5)
  - do_sample: true
  - return_dict: true
  - output_scores: true
```

**Token Generation Process**:
- Direct text completion (no chat formatting required)
- Raw logits extraction via output_scores=True parameter
- Convert logits to probabilities using torch.nn.functional.softmax()
- Top-k sampling with configurable temperature
- Token-by-token generation with full probability access
- Local inference with no external API dependencies

**Service Benefits**:
- **Independent Lifecycle**: Start/stop/restart without affecting main app
- **Resource Management**: Dedicated memory and GPU allocation
- **Performance**: Model stays loaded between requests
- **Scalability**: Can run on separate hardware/containers
- **Development**: Easier testing and debugging of ML components

### Main Application Integration

**HTTP Client Configuration**:
```
Service URL: http://localhost:8001 (configurable)
Timeout: 30 seconds (configurable)
Retry Policy: 3 attempts with exponential backoff
Health Check: Periodic service availability monitoring
```

### Frontend Framework Selection

**Reflex - Selected Framework**:
- **Pure Python Development**: Write both frontend and backend entirely in Python
- **Modern UI Components**: Leverages React and Next.js under the hood for professional appearance
- **Built-in WebSocket Support**: Real-time communication between frontend and backend
- **State Management**: Reactive state management with automatic UI updates
- **Educational Focus**: Excellent for prototyping and complex educational applications
- **Deployment**: Easy deployment with built-in development server and production options
- **Scalability**: Can scale from simple prototypes to complex applications
- **Component Library**: Rich set of pre-built components for interactive interfaces

**Radix-based Reflex Components (Current Version)**:
- **Modern Component System**: Uses Radix UI components under the hood (not Chakra UI)
- **Strict Prop Validation**: Component props have specific literal value requirements
- **Button Sizes**: `"1"`, `"2"`, `"3"`, `"4"` (not `"sm"`, `"md"`, `"lg"`)
- **Spacing Values**: `"0"` through `"9"` for spacing props in stack components
- **Grid Columns**: String literals `"1"`, `"2"`, `"3"`, etc. for grid layouts
- **CSS Props**: Standard CSS values (rem, px, %) for margin, padding, font-size, etc.
- **Type Safety**: Strict TypeScript-like prop validation prevents runtime errors

**Why Reflex is Ideal for Token Visualizer**:
- **Real-time Updates**: Built-in WebSocket support perfect for live token probability updates
- **Interactive Components**: Rich component library ideal for token selection interfaces
- **Educational UX**: Proven track record in building educational and data visualization apps
- **Python Ecosystem**: Seamless integration with Python ML/AI libraries
- **Rapid Development**: Faster development cycle compared to traditional frontend frameworks
- **Type Safety**: Radix-based prop validation ensures consistent UI behavior

### Data Flow Architecture

```
User Interaction → Reflex Frontend → Reflex State Management → Local LLM Service API
     ↑                                        ↓                        ↓
     ←―――――――――――― WebSocket Updates ←――――――――――――――――― HTTP Response
```

**Service-Oriented Flow**:
1. **User Input**: User interacts with Reflex components (buttons, text inputs)
2. **Event Handling**: Reflex event handlers trigger state updates
3. **State Management**: Reflex manages application state reactively
4. **HTTP API Calls**: Background tasks call Local LLM Service via HTTP
5. **Service Processing**: LLM Service processes request and returns probabilities
6. **State Updates**: API responses update Reflex state
7. **UI Updates**: Reflex automatically re-renders affected components via WebSocket

**Service Health Management**:
- **Health Checks**: Periodic monitoring of LLM service availability
- **Error Handling**: Graceful degradation when service is unavailable
- **Reconnection**: Automatic retry logic for failed requests
- **Status Display**: User-friendly service status indicators

## Reflex-Specific Implementation Details

### Application Structure

**Reflex App Organization**:
```
token_visualizer/                    # Main Reflex Application
├── token_visualizer/
│   ├── __init__.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── interactive_mode.py
│   │   ├── live_probability.py
│   │   ├── color_visualization.py
│   │   └── settings.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── token_display.py
│   │   ├── probability_bar.py
│   │   ├── prompt_input.py
│   │   └── navigation.py
│   ├── state/
│   │   ├── __init__.py
│   │   ├── base_state.py
│   │   ├── token_state.py
│   │   └── ui_state.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_client.py              # HTTP client for LLM service
│   │   └── health_monitor.py          # Service health monitoring
│   └── utils/
│       ├── __init__.py
│       ├── probability_calc.py
│       └── token_processing.py
├── assets/
├── requirements.txt
└── rxconfig.py

llm_service/                         # Separate LLM Service
├── main.py                          # FastAPI application entry point
├── models/
│   ├── __init__.py
│   ├── gemma_model.py              # Gemma 2 model wrapper
│   └── token_generator.py          # Token generation logic
├── api/
│   ├── __init__.py
│   ├── routes.py                   # API endpoints
│   └── schemas.py                  # Pydantic models
├── config/
│   ├── __init__.py
│   └── settings.py                 # Service configuration
├── utils/
│   ├── __init__.py
│   └── model_utils.py              # Model utilities
├── requirements.txt
└── Dockerfile                      # Container deployment
```

### State Management

**Core State Classes**:
- **TokenState**: Manages current tokens, probabilities, and generation history
- **UIState**: Handles UI state like loading indicators, error messages
- **ServiceState**: Manages LLM service connection status and health monitoring
- **SettingsState**: Application configuration and user preferences

**Reactive State Updates**:
- **Automatic Re-rendering**: Components automatically update when state changes
- **Event Handlers**: Reflex event handlers for user interactions
- **Background Tasks**: Async HTTP calls to Local LLM Service
- **State Persistence**: Optional session state persistence
- **Service Monitoring**: Real-time service health status updates

### Component Architecture

**Token Display Component**:
- **Interactive Tokens**: Clickable token buttons with hover effects
- **Probability Visualization**: Color-coded probability indicators
- **Animation Support**: Smooth transitions for token updates
- **Accessibility**: Keyboard navigation and screen reader support

**Probability Bar Component**:
- **Dynamic Bars**: Animated probability bars that update in real-time
- **Color Coding**: Visual representation of probability ranges
- **Interactive Tooltips**: Detailed probability information on hover
- **Responsive Design**: Adapts to different screen sizes

**Prompt Input Component**:
- **Rich Text Input**: Multi-line text area with syntax highlighting
- **Real-time Validation**: Input validation with immediate feedback
- **Template System**: Pre-defined prompts for educational scenarios
- **History Management**: Prompt history with easy access to previous inputs

## User Interface Design

### Layout Components

**Header Section**:
- Application title and logo
- Mode selector (tabs or dropdown)
- Settings/configuration access

**Main Content Area**:
- Prompt input field (expandable text area)
- Token display area (main visualization space)
- Probability information panel
- Control buttons (Next, Back, Reset, Export)

**Sidebar/Panel**:
- Current session statistics
- Token history
- Probability legend
- Help/tutorial access

## UI Design Principles

### Design Philosophy
Modern minimalist aesthetic inspired by ChatGPT, Gemini, and Perplexity. Focus on **intentional simplicity** where every element serves the educational mission. Eliminate visual noise to help students focus on token generation and probability visualization.

### Visual System

#### Colors
- **Light Mode**: White background (`#FFFFFF`), charcoal text (`#1A1A1A`), blue accents (`#2563EB`)
- **Dark Mode**: Near-black background (`#0F0F0F`), light gray text (`#F9F9F9`)
- **Probability Heat Map**: Red (high) → Yellow (medium) → Blue (low probability)

#### Typography
- **Primary**: Inter (clean, modern sans-serif)
- **Monospace**: JetBrains Mono (for token display)
- **Hierarchy**: 32px display, 24px titles, 16px body, 14px captions
- **Spacing**: 1.5x line height, 8px grid system

#### Iconography
- **Style**: Lucide Icons - monochromatic line icons with consistent stroke width
- **Implementation**: Using `rx.icon()` component with Lucide icon names (e.g., "zap", "activity", "palette")
- **Treatment**: 2px stroke, rounded caps, no colorful decorations
- **Sizes**: 16px (small), 20px (medium), 24px (large)
- **Color**: Inherits text color for consistency with minimal design

### Components

#### Interactive Elements
- **Buttons**: 8px radius, 44px minimum touch target, subtle hover states
- **Tokens**: Pill-shaped with gentle hover effects and color-coded probabilities
- **Inputs**: Clean borders, blue focus states, clear placeholders
- **Progress Indicators**: Simple spinner + text messages for async operations (no animated buttons, messages appear/disappear cleanly)

#### Layout
- **Desktop**: Three-column (sidebar, content, info panel)
- **Tablet**: Two-column with collapsible sidebar
- **Mobile**: Single column, bottom navigation
- **Spacing**: 8px grid system, generous white space (60/40 content ratio)

### Accessibility
- **WCAG 2.1 AA**: 4.5:1 text contrast, keyboard navigation, ARIA labels
- **Color Blind Support**: Shape/pattern indicators beyond color
- **Responsive**: Touch-friendly 44px targets, readable fonts across devices

### Responsive Design

- **Desktop**: Full-featured layout with all panels visible
- **Tablet**: Collapsible sidebar, touch-friendly controls
- **Mobile**: Simplified interface with essential features only

### Accessibility Features

- **Color Blind Support**: Alternative visualization modes
- **Keyboard Navigation**: Full keyboard control
- **Screen Reader**: Proper ARIA labels and descriptions
- **High Contrast**: Alternative color schemes

## Performance Considerations

### API Optimization

- **Caching Strategy**: Cache frequently requested token predictions
- **Batch Processing**: Group API calls when possible
- **Rate Limiting**: Respect Azure OpenAI rate limits
- **Retry Logic**: Implement exponential backoff for failed requests

### Frontend Performance

- **Reactive Updates**: Reflex's efficient state management minimizes unnecessary re-renders
- **Component Optimization**: Selective component updates based on state changes
- **WebSocket Efficiency**: Built-in WebSocket optimization for real-time updates
- **Progressive Enhancement**: Reflex components work with or without JavaScript
- **Bundle Optimization**: Reflex handles code splitting and optimization automatically

## Security & Privacy

### Data Protection

- **No Persistent Storage**: User prompts not stored long-term
- **Session Management**: Temporary storage for current session only
- **API Key Security**: Secure key storage and rotation
- **HTTPS Enforcement**: All communications encrypted

### User Privacy

- **No User Tracking**: Minimal data collection
- **Anonymous Usage**: No personal information required
- **Opt-in Analytics**: Optional usage statistics for improvement

## Deployment Strategy

### Development Environment

- **Local Development**: Python virtual environment with Reflex and dependencies
- **Configuration Management**: Environment variables for API keys and settings
- **Hot Reload**: Reflex built-in hot reload for rapid development
- **Development Server**: `reflex run` for local development with automatic reloading

### Production Deployment

**Containerization & CI/CD Pipeline**:

**Docker Container**:
- **Dockerfile**: Multi-stage build for optimized production image
- **Base Image**: Python 3.11-slim or Python 3.12-slim
- **Dependencies**: Install Reflex and all application dependencies
- **Production Build**: `reflex export --frontend-only` or full-stack build
- **Security**: Non-root user, minimal attack surface
- **Health Checks**: Container health check endpoints

**GitHub Actions CI/CD**:
- **Trigger**: Push to main branch and pull requests
- **Build Pipeline**: 
  - Lint and test Python code
  - Build Docker image
  - Security scanning with Trivy or similar
  - Push to GitHub Container Registry (ghcr.io)
- **Deployment Pipeline**:
  - Terraform plan and apply
  - Deploy to Azure Container Apps
  - Run integration tests
  - Monitor deployment health

**Container Registry**:
- **GitHub Packages**: Use GitHub Container Registry for image storage
- **Image Tagging**: Semantic versioning and Git SHA tagging
- **Security**: Automated vulnerability scanning
- **Access Control**: GitHub organization-level access management

**Infrastructure as Code (Terraform)**:

**Azure Container Apps Deployment**:
- **Terraform Configuration**: Complete infrastructure definition
- **Resource Groups**: Organized by environment (dev, staging, prod)
- **Container Apps Environment**: Shared environment for related services
- **Networking**: VNet integration for secure communication
- **Scaling**: CPU and memory-based auto-scaling rules
- **Environment Variables**: Secure injection of API keys and configuration

**Terraform Modules**:
```
terraform/
├── modules/
│   ├── container-app/
│   ├── monitoring/
│   ├── networking/
│   └── security/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
└── shared/
    └── backend.tf
```

**Monitoring & Observability**:

**OpenTelemetry Integration**:
- **Instrumentation**: Auto-instrumentation for Python/FastAPI
- **Traces**: Distributed tracing for request flows
- **Metrics**: Custom metrics for token generation, API calls, user interactions
- **Logs**: Structured logging with correlation IDs
- **Context Propagation**: Trace context across service boundaries

**Azure Monitor & Application Insights**:
- **Telemetry Export**: OpenTelemetry to Azure Monitor exporter
- **Application Map**: Visual representation of service dependencies
- **Performance Monitoring**: Response times, throughput, error rates
- **Custom Dashboards**: Token generation metrics, user engagement analytics
- **Alerts**: Proactive monitoring for service health and performance

**Deployment Workflow**:

1. **Development**: Local development with `reflex run`
2. **Code Push**: Push to GitHub triggers CI pipeline
3. **CI Pipeline**: Build, test, and push Docker image
4. **Terraform Apply**: Infrastructure deployment via GitHub Actions
5. **Container Deployment**: Azure Container Apps pulls from GitHub Packages
6. **Health Checks**: Automated deployment verification
7. **Monitoring**: OpenTelemetry data flows to Application Insights

**Security & Configuration**:
- **Secrets Management**: Azure Key Vault for API keys and sensitive data
- **Environment Variables**: Injected securely into container runtime
- **Network Security**: Private endpoints and network policies
- **Identity & Access**: Managed Identity for Azure service authentication
- **SSL/TLS**: Automatic certificate management via Azure Container Apps

## Educational Integration

### Learning Objectives

1. **Understanding Token Prediction**: Students learn how LLMs predict next tokens
2. **Probability Concepts**: Visualization of probability distributions
3. **Prompt Engineering**: See how prompt changes affect outputs
4. **Model Behavior**: Understand temperature and other parameter effects

### Teaching Materials

- **Interactive Tutorials**: Built-in guided tours
- **Example Scenarios**: Pre-configured educational examples
- **Documentation**: Explanations of concepts and terminology
- **Exercises**: Suggested activities for classroom use

### Assessment Features

- **Session Recording**: Capture student interactions for review
- **Progress Tracking**: Monitor learning objectives completion
- **Export Results**: Save visualizations for presentations

## Future Enhancements

### Advanced Features

- **Multi-model Comparison**: Compare outputs from different models
- **Custom Model Integration**: Support for fine-tuned models
- **Batch Processing**: Analyze multiple prompts simultaneously
- **Advanced Visualizations**: 3D probability landscapes, animated transitions

### Integration Possibilities

- **LMS Integration**: Connect with Learning Management Systems
- **API for Third-party**: Provide API for other educational tools
- **Mobile App**: Native mobile application
- **VR/AR Experience**: Immersive token visualization

## Success Metrics

### User Engagement

- **Session Duration**: Time spent using the application
- **Feature Usage**: Which modes are most popular
- **Return Rate**: How often users come back

### Educational Effectiveness

- **Concept Understanding**: Pre/post assessment scores
- **User Feedback**: Surveys and ratings
- **Teacher Adoption**: Usage in educational institutions

### Technical Performance

- **Response Times**: API call latency and UI responsiveness tracked via OpenTelemetry
- **Error Rates**: System reliability and uptime monitored through Azure Application Insights
- **Token Generation Metrics**: Custom metrics for token processing performance
- **Azure OpenAI API Performance**: Request/response times and success rates
- **Scalability**: Performance under various load conditions with auto-scaling metrics
- **Resource Utilization**: CPU, memory, and network usage tracked in real-time
- **User Experience Metrics**: Time-to-first-token, interactive response times

## Conclusion

The Token Visualizer represents an innovative approach to LLM education, combining interactive visualization with hands-on experimentation. By leveraging Azure OpenAI's logprobs functionality and modern web technologies, the application will provide students with an intuitive understanding of how autoregressive language models work at the token level.

The modular design allows for incremental development, starting with the core interactive token selection mode and expanding to include more advanced visualization and analysis features. The focus on educational outcomes, combined with robust technical architecture, positions this tool to make a significant impact in AI/ML education.
