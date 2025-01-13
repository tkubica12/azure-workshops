# Gradio-based Dual Chat Arena with AI Foundry and OpenTelemetry

This project demonstrates a dual-pane chat interface in Python—allowing users to interact with two separate models simultaneously. It is deployed using Terraform to Azure Container Apps. The application integrates with AI Foundry, deploying the phi-3.5 model (and others), and showcases OpenTelemetry instrumentation for monitoring and tracing.

## How It Works
- **Dual Chat Windows**: The interface provides two chatbots side by side, each with its own model selector dropdown.  
- **Model Selection**: Users can select different models for each chatbot pane, allowing side-by-side comparisons.  
- **Streaming Responses**: User messages are processed by Azure AI Foundry models via Python streaming APIs.  
- **OpenTelemetry Integration**: Application Insights collects logs and traces for monitoring and debugging.  

## Steps to Deploy
1. Install required tools (Terraform, Python, etc.).  
2. Navigate to the Terraform directory:  
   ```bash
   cd ../terraform
   terraform apply
   ```
3. Once deployment is complete, Terraform will output the Azure Container Apps endpoint.

## Connecting to the Application
1. Locate your Container Apps service in the Azure Portal. In the overview page, note the "FQDN" or "URL" field (example: 
   https://<app_name>.<region_name>.azurecontainerapps.io).
2. Open your browser and navigate to this URI.
3. You can now see the dual chat interface and try out different models.

## Observing Logs and Traces
- **Application Insights & Log Analytics**: All OpenTelemetry instrumentation data is sent to Application Insights and also stored in Log Analytics for raw analysis.  
- **Azure AI Foundry**: Logs are also surfaced directly in Azure AI Foundry, where they are aggregated and formatted for easier inspection.

## Cleaning Up
To destroy the infrastructure created by Terraform:  
```bash
cd ../terraform
terraform destroy
```

