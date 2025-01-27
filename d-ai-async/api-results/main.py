import os
import dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient, exceptions
from azure.monitor.opentelemetry import configure_azure_monitor
from azure.core.settings import settings
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI(title="AI Results", description="API to get processed results")

# Load environment variables
dotenv.load_dotenv()

def get_env_var(var_name):
    value = os.environ.get(var_name)
    if not value:
        raise EnvironmentError(f"{var_name} environment variable is not set")
    return value

cosmos_account_url = get_env_var("COSMOS_ACCOUNT_URL")
cosmos_database_name = get_env_var("COSMOS_DATABASE_NAME")
cosmos_container_name = get_env_var("COSMOS_CONTAINER_NAME")
appinsights_connection_string = get_env_var("APPLICATIONINSIGHTS_CONNECTION_STRING")

# Configure Azure Monitor
configure_azure_monitor(connection_string=appinsights_connection_string)
settings.tracing_implementation = "opentelemetry"
FastAPIInstrumentor.instrument_app(app)

# CORS
origins = [os.environ.get("CORS_ORIGIN", "*")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get CosmosDB client
credential = DefaultAzureCredential()
cosmos_client = CosmosClient(cosmos_account_url, credential)
database = cosmos_client.get_database_client(cosmos_database_name)
container = database.get_container_client(cosmos_container_name)

@app.get("/", include_in_schema=False)
def get_openapi_spec():
    return app.openapi()

@app.get(
    "/api/results/{guid}",
    response_class=JSONResponse,
    responses={
        200: {
            "description": "Result found",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "status": "completed",
                        "data": {
                            "result": "some result data"
                        }
                    }
                }
            }
        },
        202: {
            "description": "Processing, please retry after some time",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Processing, please retry after some time."
                    }
                }
            }
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error message"
                    }
                }
            }
        }
    }
)
async def get_results(guid: str):
    try:
        item = container.read_item(item=guid, partition_key=guid)
        return JSONResponse(status_code=200, content=item)
    except exceptions.CosmosResourceNotFoundError:
        return JSONResponse(status_code=202, headers={"Retry-After": "10"}, content={"message": "Processing, please retry after some time."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
