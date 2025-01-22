import os
import uuid
import dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.servicebus import ServiceBusClient, ServiceBusMessage
# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.exporter.azuremonitor import AzureMonitorTraceExporter

app = FastAPI(title="AI processing", description="API to process pictures")

# Load environment variables
dotenv.load_dotenv()
storage_account_url = os.environ.get("STORAGE_ACCOUNT_URL")
if not storage_account_url:
    raise EnvironmentError("STORAGE_ACCOUNT_URL environment variable is not set")

# CORS
origins = [os.environ.get("CORS_ORIGIN", "*")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # OpenTelemetry
# trace.set_tracer_provider(TracerProvider())
# exporter = AzureMonitorTraceExporter(
#     connection_string=os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING", "")
# )
# trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(exporter))

@app.post("/api/process")
async def process_image(file: UploadFile = File(...)):
    guid = str(uuid.uuid4())
    credential = DefaultAzureCredential()
    storage_account_client = BlobServiceClient(account_url=storage_account_url, credential=credential)
    container_client = storage_account_client.get_container_client(os.environ["STORAGE_CONTAINER"])
    blob_name = f"{guid}.jpg"
    container_client.upload_blob(name=blob_name, data=file.file, overwrite=True)
    # blob_url = f"{os.environ['BLOB_URL']}/{os.environ['BLOB_CONTAINER']}/{blob_name}"

    # servicebus_client = ServiceBusClient(os.environ["SERVICEBUS_FQDN"], credential=credential)
    # queue_sender = servicebus_client.get_queue_sender(os.environ["SERVICEBUS_QUEUE"])
    # message = ServiceBusMessage(f"New image: GUID={guid}, URL={blob_url}")
    # async with servicebus_client, queue_sender:
    #     await queue_sender.send_messages(message)

    return JSONResponse(status_code=202, content={"guid": guid})
