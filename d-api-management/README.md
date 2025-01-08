# Azure API Management Demo

This project demonstrates the capabilities of Azure API Management (APIM) using a Terraform environment to deploy APIM, a demo application, a database, monitoring, and Front Door WAF. The `src` folder contains the applications used in this demo.

## Table of Contents

- [Azure API Management Demo](#azure-api-management-demo)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Architecture](#architecture)
  - [Terraform Deployment](#terraform-deployment)
  - [Applications](#applications)
    - [auth\_entra\_api](#auth_entra_api)
    - [auth\_entra\_setup](#auth_entra_setup)
    - [auth\_entra\_web](#auth_entra_web)
    - [auth\_open\_api](#auth_open_api)
    - [bookapp\_frontend](#bookapp_frontend)
    - [books\_api](#books_api)
    - [lists\_api](#lists_api)
    - [reviews\_api](#reviews_api)
  - [Monitoring](#monitoring)
  - [Front Door WAF](#front-door-waf)

## Overview

This project showcases the use of Azure API Management to manage and secure APIs. It includes a Terraform environment to automate the deployment of the necessary infrastructure, including APIM, a demo application, a Cosmos DB database, monitoring with Azure Monitor, and a Front Door WAF for security.

## Prerequisites

- Azure Subscription
- Terraform installed
- Azure CLI installed
- Node.js and npm (for frontend application)

## Architecture

The architecture of this project includes the following components:

- **Azure API Management (APIM)**: Manages and secures the APIs.
- **Cosmos DB**: Stores the data for the demo application.
- **Azure Monitor**: Provides monitoring and logging capabilities.
- **Front Door WAF**: Provides web application firewall capabilities.
- **Demo Applications**: Various applications to demonstrate the use of APIM.

## Terraform Deployment

To deploy the infrastructure using Terraform, follow these steps:

1. Clone the repository:

   ```sh
   git clone https://github.com/your-repo/azure-api-management-demo.git
   cd azure-api-management-demo
   ```

2. Navigate to the `terraform` directory:

   ```sh
   cd terraform
   ```

3. Initialize Terraform:

    ```sh
    terraform init
    ```

4. Apply the Terraform configuration:
   
    ```sh
    terraform apply
    ```

This will deploy the APIM, Cosmos DB, Azure Monitor, Front Door WAF, and other necessary resources.  

## Applications

### auth_entra_api

This application handles authentication and authorization using Entra ID.

- **Files**:
  - .env.sample
  - `Dockerfile`
  - main.py
  - `requirements.txt`

### auth_entra_setup

This application sets up the necessary configurations for Entra ID.

- **Files**:
  - `config.py`
  - `main.py`
  - `requirements.txt`

### auth_entra_web

This is the web application for authentication using Entra ID.

- **Files**:
  - `.dockerignore`
  - `.env.sample`
  - `main.py`
  - `requirements.txt`

### auth_open_api

This application provides OpenAPI documentation for the authentication APIs.

- **Files**:
  - Various files for OpenAPI documentation

### bookapp_frontend

This is the frontend application for managing books, reviews, and lists.

- **Files**:
  - Various files for the React application

### books_api

This application provides APIs for managing books.

- **Files**:
  - Various files for the FastAPI application

### lists_api

This application provides APIs for managing lists of books.

- **Files**:
  - Various files for the FastAPI application

### reviews_api

This application provides APIs for managing book reviews.

- **Files**:
  - Various files for the FastAPI application

## Monitoring

Azure Monitor is used to provide monitoring and logging capabilities for the applications and infrastructure.

## Front Door WAF

Azure Front Door WAF is used to provide web application firewall capabilities to protect the applications from common web vulnerabilities.


