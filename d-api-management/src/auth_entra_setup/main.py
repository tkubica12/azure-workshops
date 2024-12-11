"""
Script Name: Authn and Authy demo setup of Entra ID
Author: Tomas Kubica

Description:
    This script automates the management of Azure applications through the Microsoft Graph API. 
    It includes functionalities to create main, API, and background applications with specific configurations, delete existing applications, and update environment variables accordingly. 
    The script utilizes the Azure Identity library for authentication and the Microsoft Graph SDK for application management operations.

Usage:
    Run the script directly to manage applications as defined in the `manage_applications` coroutine. This includes deleting existing applications and creating new applications with predefined settings.

Requirements:
    - Azure Identity library
    - Microsoft Graph SDK
    - An Azure account with permissions to manage applications
"""

import asyncio
from azure.identity import DefaultAzureCredential
from msgraph import GraphServiceClient
from msgraph.generated.models.application import Application
from msgraph.generated.models.api_application import ApiApplication
from msgraph.generated.models.permission_scope import PermissionScope
from msgraph.generated.models.web_application import WebApplication
from msgraph.generated.models.required_resource_access import RequiredResourceAccess
from msgraph.generated.models.resource_access import ResourceAccess
from msgraph.generated.models.service_principal import ServicePrincipal
from msgraph.generated.applications.applications_request_builder import ApplicationsRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from msgraph.generated.models.password_credential import PasswordCredential
import os
from config import config  # Import configuration

env_file_path = config["env_file_path"]
api_client_id = None


def update_env_field(env_file_path, field_name, field_value):
    """
    Updates or adds a field in the specified .env file.

    Parameters:
        env_file_path (str): Path to the .env file.
        field_name (str): The name of the environment variable to update or add.
        field_value (str): The value to set for the environment variable.
    """
    # Ensure the .env file exists, create if not
    if not os.path.exists(env_file_path):
        with open(env_file_path, 'w') as file:
            file.write(f"{field_name}={field_value}\n")
        return

    # Read the existing content
    with open(env_file_path, 'r') as file:
        lines = file.readlines()

    # Update or add the specified field
    updated_lines = []
    field_updated = False
    for line in lines:
        if line.startswith(f"{field_name}="):
            updated_lines.append(f"{field_name}={field_value}\n")
            field_updated = True
        else:
            updated_lines.append(line)

    if not field_updated:
        updated_lines.append(f"{field_name}={field_value}\n")

    # Write the updated content back to the .env file
    with open(env_file_path, 'w') as file:
        file.writelines(updated_lines)


async def create_main_application():
    """
    Creates the main application with predefined settings and updates the .env file with its credentials.
    """
    # Initialize DefaultAzureCredential
    credentials = DefaultAzureCredential()

    # Initialize GraphClient with the credential
    graph_client = GraphServiceClient(credentials=credentials)

    # Define the application request body
    request_body = Application(
        display_name=config["applications"]["main"]["display_name"],  # Updated reference
        sign_in_audience="AzureADMyOrg ",
        password_credentials=[
            PasswordCredential(
                display_name="mypassword",
            ),
        ],
        group_membership_claims="SecurityGroup",
        web=WebApplication(
            redirect_uris=config["applications"]["main"]["redirect_uris"]  # Updated reference
        )
    )

    result = await graph_client.applications.post(request_body)
    update_env_field(env_file_path, "MAIN_CLIENT_ID", result.app_id)
    update_env_field(env_file_path, "MAIN_CLIENT_SECRET",
                     result.password_credentials[0].secret_text)
    print(f"Created Main application: {result.app_id}")


async def create_api_application():
    """
    Creates the API application with predefined settings, including permission scopes, and updates the .env file with its credentials.
    """
    # Initialize DefaultAzureCredential
    credentials = DefaultAzureCredential()

    # Initialize GraphClient with the credential
    graph_client = GraphServiceClient(credentials=credentials)

    # Define the application request body
    request_body = Application(
        display_name=config["applications"]["api"]["display_name"],
        sign_in_audience="AzureADMyOrg ",
        password_credentials=[
            PasswordCredential(
                display_name="mypassword",
            ),
        ],
        group_membership_claims="SecurityGroup",
        identifier_uris=["api://tokubica-auth-entra-api"],
        web=WebApplication(
            redirect_uris=config["applications"]["api"]["redirect_uris"]  # Updated reference
        ),
        api=ApiApplication(
            requested_access_token_version=2,
            oauth2_permission_scopes=[
                PermissionScope(
                    admin_consent_description="Allows application to read information about your stuff",
                    admin_consent_display_name="Read your custom stuff",
                    id=config["applications"]["api"]["permission_scopes"]["read"]["id"],
                    is_enabled=True,
                    type="User",
                    user_consent_description="Allows application to read information about your stuff",
                    user_consent_display_name="Read your custom stuff",
                    value="Stuff.Read"
                ),
                PermissionScope(
                    admin_consent_description="Allows application to write information about your stuff",
                    admin_consent_display_name="Write your custom stuff",
                    id=config["applications"]["api"]["permission_scopes"]["write"]["id"],
                    is_enabled=True,
                    type="User",
                    user_consent_description="Allows application to write information about your stuff",
                    user_consent_display_name="Write your custom stuff",
                    value="Stuff.Write"
                )
            ]
        )
    )

    result = await graph_client.applications.post(request_body)
    update_env_field(env_file_path, "API_CLIENT_ID", result.app_id)
    update_env_field(env_file_path, "API_CLIENT_SECRET",
                     result.password_credentials[0].secret_text)
    global api_client_id
    api_client_id = result.app_id
    print(f"Created API application: {result.app_id}")

    # Create a service principal for the API application
    request_body = ServicePrincipal(
        app_id = result.app_id,
    )
    result = await graph_client.service_principals.post(request_body)
    print(f"Created API Service Principal: {result.id}")


async def create_apim_application():
    """
    Creates the background application with predefined settings, including required resource access to the API application, and updates the .env file with its credentials.
    """
    # Initialize DefaultAzureCredential
    credentials = DefaultAzureCredential()

    # Initialize GraphClient with the credential
    graph_client = GraphServiceClient(credentials=credentials)

    # Define the application request body
    request_body = Application(
        display_name=config["applications"]["apim"]["display_name"],
        sign_in_audience="AzureADMyOrg ",
        password_credentials=[
            PasswordCredential(
                display_name="mypassword",
            ),
        ],
        required_resource_access=[
            RequiredResourceAccess(
                resource_app_id=api_client_id,
                resource_access=[
                    ResourceAccess(
                        id=config["applications"]["api"]["permission_scopes"]["read"]["id"],  # Referenced from config
                        type="Scope"
                    )
                ]
            )
        ]
    )

    result = await graph_client.applications.post(request_body)
    update_env_field(env_file_path, "APIM_CLIENT_ID", result.app_id)
    update_env_field(env_file_path, "APIM_CLIENT_SECRET",
                     result.password_credentials[0].secret_text)
    print(f"Created APIM application: {result.app_id}")

    # Create a service principal for the background application
    request_body = ServicePrincipal(
        app_id = result.app_id,
    )
    result = await graph_client.service_principals.post(request_body)
    print(f"Created APIM Service Principal: {result.id}")

async def create_background_application():
    """
    Creates the background application with predefined settings, including required resource access to the API application, and updates the .env file with its credentials.
    """
    # Initialize DefaultAzureCredential
    credentials = DefaultAzureCredential()

    # Initialize GraphClient with the credential
    graph_client = GraphServiceClient(credentials=credentials)

    # Define the application request body
    request_body = Application(
        display_name=config["applications"]["background"]["display_name"],
        sign_in_audience="AzureADMyOrg ",
        password_credentials=[
            PasswordCredential(
                display_name="mypassword",
            ),
        ],
        required_resource_access=[
            RequiredResourceAccess(
                resource_app_id=api_client_id,
                resource_access=[
                    ResourceAccess(
                        id=config["applications"]["api"]["permission_scopes"]["read"]["id"],  # Referenced from config
                        type="Scope"
                    )
                ]
            )
        ]
    )

    result = await graph_client.applications.post(request_body)
    update_env_field(env_file_path, "BACKGROUND_CLIENT_ID", result.app_id)
    update_env_field(env_file_path, "BACKGROUND_CLIENT_SECRET",
                     result.password_credentials[0].secret_text)
    print(f"Created Background application: {result.app_id}")

    # Create a service principal for the background application
    request_body = ServicePrincipal(
        app_id = result.app_id,
    )
    result = await graph_client.service_principals.post(request_body)
    print(f"Created Background Service Principal: {result.id}")


async def delete_applications_by_name(app_name):
    """
    Deletes applications by display name.

    Parameters:
        app_name (str): The display name of the applications to delete.
    """
    # Initialize DefaultAzureCredential for authentication
    credentials = DefaultAzureCredential()
    # Create a GraphServiceClient instance with the credentials
    graph_client = GraphServiceClient(credentials)

    # Prepare query parameters to filter applications by display name
    query_params = ApplicationsRequestBuilder.ApplicationsRequestBuilderGetQueryParameters(
        filter=f"displayName eq '{app_name}'"
    )

    # Configure request with query parameters and headers
    request_configuration = RequestConfiguration(
        query_parameters=query_params
    )

    # Add header for eventual consistency level
    request_configuration.headers.add("ConsistencyLevel", "eventual")

    # Fetch applications matching the filter criteria
    applications = await graph_client.applications.get(request_configuration=request_configuration)
    # Iterate over the fetched applications and delete each one
    for application in applications.value:
        await graph_client.applications.by_application_id(application.id).delete()
        print(f"Deleted application: {application.id}")

# Orchestrate the application management operations
async def manage_applications():
    await delete_applications_by_name(config["applications"]["main"]["display_name"])
    await delete_applications_by_name(config["applications"]["api"]["display_name"])
    await delete_applications_by_name(config["applications"]["apim"]["display_name"])
    await delete_applications_by_name(config["applications"]["background"]["display_name"])
    await create_main_application()
    await create_api_application()
    await create_apim_application()
    await create_background_application()

if __name__ == "__main__":
    asyncio.run(manage_applications())
