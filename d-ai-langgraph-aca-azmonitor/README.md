# Multi-agent Lang Graph example with UI, OpenTelemetry, Azure Monitor and Container Apps

## What is this?
This repository is a hands‑on demo of a **LangGraph‑based AI multi‑agent system** exposed through a **Streamlit** UI.  
The demo shows how to:

* Orchestrate several specialized agents (fun planner, budget planner, practical planner, foodie, writer, finisher) with a **supervisor** agent using [LangGraph](https://github.com/langchain-ai/langgraph).  
* Let the agents collaborate to build a coherent travel itinerary document, iterating until the supervisor decides the task is complete.  
* Capture the entire conversation (logs, traces, custom metrics) with **OpenTelemetry** and forward it either to a local Aspire dashboard or to **Azure Application Insights** when deployed to **Azure Container Apps**.  
* Package the workload in a single container image that you can run locally or deploy to ACA.

High‑level flow:

1. A user asks a travel planning question in the Streamlit UI.  
2. The supervisor agent decides which domain agent should answer next and what to ask them.  
3. Agents reply, the supervisor routes the conversation, and periodically invokes the *writer* agent to update the Markdown itinerary.  
4. When satisfied, the supervisor hands off to the *finish* agent which produces the final summary.  
5. All agent messages are logged and exported via OTEL; a custom counter (`agent_message_count`) tracks how many messages each agent produced.

## Monitoring
### Local Aspire dashboard
In ```.env``` file set OTEL_EXPORTER_OTLP_ENDPOINT to ```http://localhost:4317```. To access dashboard see logs from Aspire container start with URL with key.

```powershell
docker run --rm -it `
-p 18888:18888 `
-p 4317:18889 `
--name aspire-dashboard `
mcr.microsoft.com/dotnet/aspire-dashboard:latest
```

Run application and see it collecting:
- Logs from appp
- Traces that include LLM calls with input and output texts
- Metrics including autoinstrumented token counts and also custom "agent message count" metric

### Azure Container Apps (Application Insights)
When you deploy to Azure Container Apps, the managed environment includes a built‑in OpenTelemetry collector. It automatically injects the necessary OTEL_* env vars into each container and can be configured to route telemetry to various backends. In this workshop we’ve enabled Application Insights via the `appInsightsConfiguration` block.

Key points:
- The collector streams **logs** and **traces** to your Application Insights instance.
- Required env vars (injected by ACA):
  - OTEL_EXPORTER_OTLP_PROTOCOL=grpc  
  - OTEL_TRACES_EXPORTER=console,otlp  
  - OTEL_EXPORTER_OTLP_ENDPOINT (collector endpoint)  
- Metrics forwarding is not yet supported by the ACA OTEL collector.

To configure:
1. In `container_app_env.tf` set `appInsightsConfiguration.connectionString` to your AI connection string.
2. The collector will pick this up and begin streaming logs/traces automatically.

## Infrastructure (Terraform)
The `/terraform` folder provisions all Azure resources required to run the demo:

| Layer | Main resources |
|-------|----------------|
| Core | **Resource Group** (`rg-…`) and **random_string** used for unique names |
| Networking / Storage | **Storage Account** (blob access only) – used by AI Hub for artifact storage |
| Security | **Key Vault** – secrets for the hub / models<br/>Role assignments giving the current user and the AI Hub managed identity *Blob Data Owner* access |
| Observability | **Log Analytics Workspace** + **Application Insights**.  ACA environment is wired to AI via `appInsightsConfiguration` and its built‑in OTEL collector streams *traces* and *logs*. |
| AI services | **Azure AI Services (OpenAI)** account (`aidemo‑…`) with three model deployments (`gpt‑4.1`, `gpt‑4.1‑mini`, `gpt‑4.1‑nano`).<br/>**AI Hub & AI Project** resources that reference the storage, key‑vault and insights instances. |
| Compute | **Container App Environment** with OTEL and log routing enabled.<br/>A single **Container App** running the Streamlit multi‑agent app.  Model endpoints & keys are injected from Terraform output `local.model_configurations`. |

All resources are created in the region defined by `var.location` (default `swedencentral`).  
Run:

```bash
cd terraform
terraform init
terraform apply   # review & approve
```

to deploy the full stack, then grab the Container App URL from the outputs and open it in your browser.

### TODO / Next steps
- 🗂 **Distributed deployment** – package every agent (fun, budget, practical, foodie, writer, finish, supervisor) as an individual Container App so that they can scale independently.  
- 🔄 **Agent‑to‑Agent (A2A) protocol** – migrate inter‑agent calls to the upcoming ACA A2A registry & protocol when it becomes generally available, eliminating direct HTTP endpoints.  
- 🏷 **Service registry** – register each agent instance with the A2A registry to enable dynamic discovery and routing by the supervisor.  
- 📈 **Event‑sourced telemetry** – persist all agent events (messages, state changes) to an event‑sourcing store (e.g., Azure Cosmos DB or Event Hubs) for replay and audit.  
- 📊 **Enhanced UI observability** – extend the Streamlit front‑end with real‑time charts fed from the event store (message throughput, per‑agent latencies, conversation timelines).  
- 🚀 **Auto‑scaling policies** – configure per‑agent scale rules (CPU / queue length) so workload spikes are handled efficiently.

