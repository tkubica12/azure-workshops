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
- **Cloud Service**: Azure OpenAI Service
- **Authentication**: Azure Active Directory (AAD)
- **API Integration**: Azure OpenAI REST API with logprobs enabled
- **Framework**: Integrated with Reflex's built-in FastAPI backend

### Frontend
- **Technology**: Reflex Python Framework
- **Architecture**: Full-stack Python development with React/Next.js under the hood
- **Interface**: Web-based interactive UI with modern components
- **Real-time Updates**: Built-in WebSocket communication between frontend and backend

### Authentication & Security
- **Azure AD Integration**: Secure access to Azure OpenAI
- **User Management**: Optional user sessions for personalized experience
- **API Key Management**: Secure storage and rotation of API keys

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

### Azure OpenAI Integration

**API Configuration**:
```
Endpoint: Azure OpenAI endpoint URL
Model: gpt-4.1-nano
Parameters:
  - max_tokens: configurable (default: 1)
  - logprobs: true
  - top_logprobs: 5
  - temperature: configurable (default: 0.7)
```

**Response Processing**:
- Extract logprobs from response
- Convert log probabilities to percentages
- Handle token decoding and display formatting
- Error handling for API failures

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

**Why Reflex is Ideal for Token Visualizer**:
- **Real-time Updates**: Built-in WebSocket support perfect for live token probability updates
- **Interactive Components**: Rich component library ideal for token selection interfaces
- **Educational UX**: Proven track record in building educational and data visualization apps
- **Python Ecosystem**: Seamless integration with Python ML/AI libraries
- **Rapid Development**: Faster development cycle compared to traditional frontend frameworks

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

### Real-time Features

**WebSocket Integration**:
- **Live Updates**: Instant UI updates as tokens are generated
- **Progress Indicators**: Real-time progress for long-running operations
- **Error Handling**: Graceful handling of connection issues
- **Reconnection Logic**: Automatic reconnection on network issues

**Performance Optimizations**:
- **Debounced Updates**: Prevent excessive API calls during rapid input changes
- **Selective Re-rendering**: Only update components that have changed
- **Lazy Loading**: Load components and data as needed
- **Caching**: Client-side caching of frequently accessed data

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

## DevOps & Infrastructure

### Dockerfile Specification

**Multi-stage Dockerfile**:
```dockerfile
# Build stage
FROM python:3.12-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN reflex export --frontend-only

# Production stage
FROM python:3.12-slim
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app
COPY --from=builder /app/.web/_static ./static
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=builder /app .
RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
CMD ["reflex", "run", "--env", "prod", "--backend-only"]
```

### GitHub Actions Workflows

**CI/CD Pipeline** (`.github/workflows/deploy.yml`):
```yaml
name: Build and Deploy
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest black flake8
      - name: Lint and test
        run: |
          black --check .
          flake8 .
          pytest tests/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:latest
            ghcr.io/${{ github.repository }}:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
      - name: Terraform Apply
        env:
          ARM_CLIENT_ID: ${{ secrets.ARM_CLIENT_ID }}
          ARM_CLIENT_SECRET: ${{ secrets.ARM_CLIENT_SECRET }}
          ARM_SUBSCRIPTION_ID: ${{ secrets.ARM_SUBSCRIPTION_ID }}
          ARM_TENANT_ID: ${{ secrets.ARM_TENANT_ID }}
        run: |
          cd terraform/environments/prod
          terraform init
          terraform plan
          terraform apply -auto-approve
```

### Terraform Infrastructure

**Main Container App Configuration** (`terraform/modules/container-app/main.tf`):
```hcl
resource "azurerm_container_app" "token_visualizer" {
  name                         = var.app_name
  container_app_environment_id = var.container_app_environment_id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"

  template {
    min_replicas = 1
    max_replicas = 10

    container {
      name   = "token-visualizer"
      image  = var.container_image
      cpu    = 0.5
      memory = "1Gi"

      env {
        name  = "AZURE_OPENAI_ENDPOINT"
        value = var.azure_openai_endpoint
      }

      env {
        name        = "AZURE_OPENAI_API_KEY"
        secret_name = "azure-openai-key"
      }

      env {
        name  = "APPLICATIONINSIGHTS_CONNECTION_STRING"
        value = var.app_insights_connection_string
      }
    }
  }

  secret {
    name  = "azure-openai-key"
    value = var.azure_openai_api_key
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    traffic_weight {
      percentage = 100
      latest_revision = true
    }
  }
}
```

**Monitoring Configuration** (`terraform/modules/monitoring/main.tf`):
```hcl
resource "azurerm_application_insights" "token_visualizer" {
  name                = "${var.app_name}-insights"
  location            = var.location
  resource_group_name = var.resource_group_name
  application_type    = "web"
  retention_in_days   = 90

  tags = var.tags
}

resource "azurerm_monitor_action_group" "alerts" {
  name                = "${var.app_name}-alerts"
  resource_group_name = var.resource_group_name
  short_name          = "tokenvis"

  email_receiver {
    name          = "admin"
    email_address = var.admin_email
  }
}

resource "azurerm_monitor_metric_alert" "high_response_time" {
  name                = "High Response Time"
  resource_group_name = var.resource_group_name
  scopes              = [azurerm_application_insights.token_visualizer.id]
  description         = "Alert when response time is high"

  criteria {
    metric_namespace = "microsoft.insights/components"
    metric_name      = "requests/duration"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 5000
  }

  action {
    action_group_id = azurerm_monitor_action_group.alerts.id
  }
}
```

### OpenTelemetry Configuration

**Python Application Setup**:
```python
# config/telemetry.py
from opentelemetry import trace, metrics
from opentelemetry.exporter.azuremonitor import AzureMonitorTraceExporter, AzureMonitorMetricsExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

def setup_telemetry(app, connection_string: str):
    # Tracing
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)
    
    trace_exporter = AzureMonitorTraceExporter(
        connection_string=connection_string
    )
    span_processor = BatchSpanProcessor(trace_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
    
    # Metrics
    metrics_exporter = AzureMonitorMetricsExporter(
        connection_string=connection_string
    )
    metric_reader = PeriodicExportingMetricReader(
        exporter=metrics_exporter,
        export_interval_millis=60000
    )
    metrics.set_meter_provider(MeterProvider(metric_readers=[metric_reader]))
    
    # Auto-instrumentation
    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()
    
    return tracer
```

**Custom Metrics for Token Visualization**:
```python
# services/metrics.py
from opentelemetry import metrics
from typing import Dict, Any

class TokenVisualizerMetrics:
    def __init__(self):
        meter = metrics.get_meter(__name__)
        
        # Counters
        self.token_generations = meter.create_counter(
            "token_generations_total",
            description="Total number of token generations"
        )
        
        self.api_calls = meter.create_counter(
            "azure_openai_calls_total",
            description="Total Azure OpenAI API calls"
        )
        
        # Histograms
        self.response_time = meter.create_histogram(
            "response_time_seconds",
            description="Response time for token generation"
        )
        
        self.token_probability = meter.create_histogram(
            "token_probability_distribution",
            description="Distribution of token probabilities"
        )
    
    def record_token_generation(self, mode: str, tokens_count: int):
        self.token_generations.add(1, {"mode": mode, "tokens": tokens_count})
    
    def record_api_call(self, model: str, success: bool):
        self.api_calls.add(1, {"model": model, "success": str(success)})
    
    def record_response_time(self, operation: str, duration: float):
        self.response_time.record(duration, {"operation": operation})
```

### Environment Management

**Environment Variables**:
```bash
# Production environment variables
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=your-key
ENVIRONMENT=production
LOG_LEVEL=INFO
```

**Configuration Management**:
```python
# config/settings.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_openai_api_version: str = "2024-02-15-preview"
    applicationinsights_connection_string: Optional[str] = None
    environment: str = "development"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
```
