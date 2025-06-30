# Token Visualizer Design Document

## Overview

The Token Visualizer is an educational application designed to help students understand autoregressive Large Language Models (LLMs) from the perspective of next token prediction. The application provides interactive visualization of token generation probabilities using Azure OpenAI service with logprobs functionality.

## Objectives

- **Educational Focus**: Help students understand how LLMs work at the token level
- **Interactive Learning**: Provide hands-on experience with token selection and probability visualization
- **Real-time Feedback**: Show how prompt modifications affect token probabilities
- **Visual Understanding**: Use colors, probabilities, and interactive elements to make abstract concepts concrete

## Architecture Overview

### Backend
- **Technology**: Python
- **Local LLM**: Google Gemma 2 2B base model
- **ML Framework**: Hugging Face Transformers
- **Inference**: Local GPU/CPU inference (PyTorch)
- **Framework**: Integrated with Reflex's built-in FastAPI backend

### Frontend
- **Technology**: Reflex Python Framework
- **Architecture**: Full-stack Python development with React/Next.js under the hood
- **Interface**: Web-based interactive UI with modern components
- **Real-time Updates**: Built-in WebSocket communication between frontend and backend

**CRITICAL - Reflex Component Props:**
- **Spacing Values**: MUST use string literals `"0"` to `"9"` (NOT CSS values like `"1rem"`)
- **Size Values**: MUST use string literals `"1"` to `"9"` (NOT CSS values)
- **Prop Validation**: Reflex enforces strict prop types - always check existing working code
- **Common Error**: `TypeError: Invalid var passed for prop VStack.spacing` indicates wrong prop type

### Local LLM Integration
- **Model**: Google Gemma 2 2B base model via Hugging Face
- **Inference Engine**: Transformers library with AutoModelForCausalLM
- **Hardware**: Local GPU (CUDA) or CPU fallback
- **Logits Access**: Direct logits extraction via output_scores=True

## Core Features & Modes

### Mode 1: Interactive Token-by-Token Generation

**Description**: The primary mode where users experience step-by-step token generation with choice selection.

**User Flow**:
1. User enters an initial prompt
2. System calls Azure OpenAI with logprobs=5 to get top 5 token alternatives
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
- Efficient API call management to minimize latency
- Reflex state management for current context and token history
- Reactive UI components for token selection
- Background task handling for API calls

### Mode 2: Live Probability Visualization

**Description**: Real-time visualization of how prompt modifications affect response probabilities.

**User Flow**:
1. User enters a base prompt (e.g., "What is the capital of France?")
2. System generates initial response with probabilities
3. User modifies prompt (e.g., adds "You are a clever professor" or "You are very funny")
4. System immediately re-generates response showing probability changes
5. Visual comparison shows before/after probability distributions

**Features**:
- **Side-by-side Comparison**: Original vs. modified prompt results
- **Probability Difference Highlighting**: Show increases/decreases in token probabilities
- **Real-time Updates**: Minimal delay between prompt change and result update
- **Prompt Templates**: Pre-defined prompt modifications for common scenarios

**Technical Requirements**:
- Debounced API calls to handle rapid prompt changes (using Reflex event handlers)
- Efficient diff calculation for probability changes
- Smooth UI transitions for probability updates (built-in Reflex animations)
- Real-time state synchronization via WebSocket

### Mode 3: Color-coded Token Visualization

**Description**: Visual representation of token probabilities through color intensity and patterns.

**Features**:
- **Heat Map Visualization**: Tokens colored by probability (high = warm colors, low = cool colors)
- **Gradient Representation**: Smooth color transitions showing probability distributions
- **Interactive Hover**: Detailed probability information on token hover
- **Color Customization**: Different color schemes for accessibility
- **Export Options**: Save visualizations as images

**Visual Design**:
- **Color Scale**: Red (high probability) → Yellow (medium) → Blue (low probability)
- **Transparency**: Lower probability tokens shown with reduced opacity
- **Typography**: Clear, readable fonts with good contrast

### Mode 4: Interactive Token Tree (Future Enhancement)

**Description**: Advanced visualization showing branching paths of possible token sequences.

**Concept**:
- Tree structure showing multiple possible paths
- Interactive navigation through different branches
- Probability-weighted branch thickness
- Collapsible nodes for complexity management

## Technical Specifications

### Local LLM Integration

**Model Configuration**:
```
Model: google/gemma-2-2b (base model)
Framework: Hugging Face Transformers
Hardware: Local GPU (CUDA preferred) or CPU
Memory: ~5GB GPU VRAM or 8GB+ system RAM
Parameters:
  - max_new_tokens: configurable (default: 1)
  - temperature: configurable (default: 0.7)
  - top_k: configurable (default: 5)
  - do_sample: true
```

**Token Generation Process**:
- Direct text completion (no chat formatting required)
- Raw logits extraction via output_scores=True parameter
- Convert logits to probabilities using torch.nn.functional.softmax()
- Top-k sampling with configurable temperature
- Token-by-token generation with full probability access
- Local inference with no API dependencies

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
User Interaction → Reflex Frontend → Reflex State Management → Azure OpenAI API
     ↑                                        ↓                        ↓
     ←―――――――――――― WebSocket Updates ←――――――――――――――――― Process Response
```

**Reflex-Specific Flow**:
1. **User Input**: User interacts with Reflex components (buttons, text inputs)
2. **Event Handling**: Reflex event handlers trigger state updates
3. **State Management**: Reflex manages application state reactively
4. **API Calls**: Background tasks call Azure OpenAI API
5. **State Updates**: API responses update Reflex state
6. **UI Updates**: Reflex automatically re-renders affected components via WebSocket

## Reflex-Specific Implementation Details

### Application Structure

**Reflex App Organization**:
```
token_visualizer/
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
│   │   ├── azure_openai.py
│   │   └── auth.py
│   └── utils/
│       ├── __init__.py
│       ├── probability_calc.py
│       └── token_processing.py
├── assets/
├── requirements.txt
└── rxconfig.py
```

### State Management

**Core State Classes**:
- **TokenState**: Manages current tokens, probabilities, and generation history
- **UIState**: Handles UI state like loading indicators, error messages
- **AuthState**: Manages Azure AD authentication and API credentials
- **SettingsState**: Application configuration and user preferences

**Reactive State Updates**:
- **Automatic Re-rendering**: Components automatically update when state changes
- **Event Handlers**: Reflex event handlers for user interactions
- **Background Tasks**: Async API calls to Azure OpenAI
- **State Persistence**: Optional session state persistence

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
