from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from azure.identity import DefaultAzureCredential
import os
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from dotenv import load_dotenv
import json
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from azure.core.settings import settings
from azure.monitor.opentelemetry import configure_azure_monitor

app = FastAPI(title="Lists", description="API to manage lists of books")
load_dotenv()

configure_azure_monitor()

# Initialize CosmosDB client
credential = DefaultAzureCredential()
cosmos_endpoint = os.environ.get("COSMOSDB_ENDPOINT")
cosmos_client = CosmosClient(cosmos_endpoint, credential)
database_name = "BooksApp"
container_name = "Lists"

# Create database and container if they don't exist
database = cosmos_client.create_database_if_not_exists(id=database_name)
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/id")
)

@app.get("/", include_in_schema=False)
def get_openapi_spec():
    return app.openapi()

class BooksList(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    books: List[str] = []

@app.post(
    "/lists/",
    response_model=BooksList,
    responses={
        200: {
            "description": "The created list",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "Favorite Books",
                        "description": "A list of my favorite books.",
                        "books": ["Book One", "Book Two"]
                    }
                }
            }
        },
        400: {"description": "Invalid input"}
    }
)
def create_list(list: BooksList):
    """
    Create a new list.

    Args:
        list (BooksList): The list to create.

    Returns:
        BooksList: The created list.
    """
    list.id = str(uuid.uuid4())
    container.create_item(body=list.dict())
    return list

@app.get(
    "/lists/",
    response_model=List[BooksList],
    responses={
        200: {
            "description": "A list of lists",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "name": "Favorite Books",
                            "description": "A list of my favorite books.",
                            "books": ["Book One", "Book Two"]
                        }
                    ]
                }
            }
        },
        400: {"description": "Invalid input"}
    }
)
def read_lists(skip: int = 0, limit: int = 10):
    """
    Retrieve a list of lists.

    Args:
        skip (int): Number of lists to skip.
        limit (int): Maximum number of lists to return.

    Returns:
        List[BooksList]: A list of lists.
    """
    query = f"SELECT * FROM c OFFSET {skip} LIMIT {limit}"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return items

@app.get(
    "/lists/{list_id}",
    response_model=BooksList,
    responses={
        200: {
            "description": "The retrieved list",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "Favorite Books",
                        "description": "A list of my favorite books.",
                        "books": ["Book One", "Book Two"]
                    }
                }
            }
        },
        404: {"description": "List not found"}
    }
)
def read_list(list_id: str):
    """
    Retrieve a list by its ID.

    Args:
        list_id (str): The ID of the list to retrieve.

    Returns:
        BooksList: The retrieved list.
    """
    try:
        item = container.read_item(item=list_id, partition_key=list_id)
        return item
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="List not found")

@app.put(
    "/lists/{list_id}",
    response_model=BooksList,
    responses={
        200: {
            "description": "The updated list",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "Updated List",
                        "description": "An updated description.",
                        "books": ["Book One", "Book Two", "Book Three"]
                    }
                }
            }
        },
        404: {"description": "List not found"},
        400: {"description": "Invalid input"}
    }
)
def update_list(list_id: str, updated_list: BooksList):
    """
    Update a list by its ID.

    Args:
        list_id (str): The ID of the list to update.
        updated_list (BooksList): The updated list data.

    Returns:
        BooksList: The updated list.
    """
    try:
        item = container.read_item(item=list_id, partition_key=list_id)
        updated_data = updated_list.dict(exclude_unset=True)
        item.update(updated_data)
        container.replace_item(item=list_id, body=item)
        return item
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="List not found")
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

@app.delete(
    "/lists/{list_id}",
    response_model=BooksList,
    responses={
        200: {
            "description": "The deleted list",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "Deleted List",
                        "description": "This list has been deleted.",
                        "books": ["Book One", "Book Two"]
                    }
                }
            }
        },
        404: {"description": "List not found"}
    }
)
def delete_list(list_id: str):
    """
    Delete a list by its ID.

    Args:
        list_id (str): The ID of the list to delete.

    Returns:
        BooksList: The deleted list.
    """
    try:
        item = container.read_item(item=list_id, partition_key=list_id)
        container.delete_item(item=list_id, partition_key=list_id)
        return item
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="List not found")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )

# OpenTelemetry instrumentation
settings.tracing_implementation = "opentelemetry"
FastAPIInstrumentor.instrument_app(app)