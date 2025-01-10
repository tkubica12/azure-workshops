# Gradio-based Chat Interface with AI Foundry and OpenTelemetry

This project demonstrates a Gradio-based chat interface in Python, deployed using Terraform to Azure Container Apps. It integrates with AI Foundry, deploying the phi-3.5 model, and showcases OpenTelemetry instrumentation for monitoring and tracing.

## Features

- **Gradio Chat Interface**: A user-friendly chat interface built with Gradio.
- **AI Foundry Integration**: Deployment of the phi-3.5 model for AI inference using Terraform.
- **Azure Container Apps**: Deployment using Terraform to Azure Container Apps.
- **OpenTelemetry Instrumentation**: Monitoring and tracing with Application Insights.

## Deploy
To deploy the project, follow the steps below:
```sh
cd ../terraform
terraform apply
```

## Cleaning Up

To destroy the infrastructure created by Terraform:
```sh
cd ../terraform
terraform destroy
```

