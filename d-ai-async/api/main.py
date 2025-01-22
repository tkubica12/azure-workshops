import os
import uuid
import dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import json
# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.exporter.azuremonitor import AzureMonitorTraceExporter

app = FastAPI(title="AI processing", description="API to process pictures")

# Load environment variables
dotenv.load_dotenv()

def get_env_var(var_name):
    value = os.environ.get(var_name)
    if not value:
        raise EnvironmentError(f"{var_name} environment variable is not set")
    return value

storage_account_url = get_env_var("STORAGE_ACCOUNT_URL")
storage_container = get_env_var("STORAGE_CONTAINER")
processed_base_url = get_env_var("PROCESSED_BASE_URL")
servicebus_fqdn = get_env_var("SERVICEBUS_FQDN")
servicebus_queue = get_env_var("SERVICEBUS_QUEUE")

# CORS
origins = [os.environ.get("CORS_ORIGIN", "*")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

credential = DefaultAzureCredential()
storage_account_client = BlobServiceClient(account_url=storage_account_url, credential=credential)
container_client = storage_account_client.get_container_client(storage_container)
servicebus_client = ServiceBusClient(servicebus_fqdn, credential=credential)
servicebus_queue = servicebus_client.get_queue_sender(servicebus_queue)

# # OpenTelemetry
# trace.set_tracer_provider(TracerProvider())
# exporter = AzureMonitorTraceExporter(
#     connection_string=os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING", "")
# )
# trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(exporter))

@app.post("/api/process")
async def process_image(file: UploadFile = File(...)):
    # Generate GUID
    guid = str(uuid.uuid4())

    # Upload image to storage
    blob_name = f"{guid}.jpg"
    container_client.upload_blob(name=blob_name, data=file.file, overwrite=False)

    # Send message to Service Bus
    blob_url = f"{storage_account_url}/{storage_container}/{blob_name}"
    message = ServiceBusMessage(json.dumps({"blob_url": blob_url}))
    servicebus_queue.send_messages(message)


    return JSONResponse(status_code=202, content={"id": guid, "results_url": f"{processed_base_url}/{guid}"})
