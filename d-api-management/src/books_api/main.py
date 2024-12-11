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

configure_azure_monitor()
app = FastAPI(title="Books", description="API to manage books")
load_dotenv()

# Initialize CosmosDB client
credential = DefaultAzureCredential()
cosmos_endpoint = os.environ.get("COSMOSDB_ENDPOINT")
cosmos_client = CosmosClient(cosmos_endpoint, credential)
database_name = "BooksApp"
container_name = "Books"

# Create database and container if they don't exist
database = cosmos_client.create_database_if_not_exists(id=database_name)
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/id")
)

@app.get("/", include_in_schema=False)
def get_openapi_spec():
    return app.openapi()

class Book(BaseModel):
    id: Optional[str] = None
    title: str
    author: str
    description: Optional[str] = None

@app.post(
    "/books/",
    response_model=Book,
    responses={
        200: {
            "description": "The created book",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123",
                        "title": "Example Book",
                        "author": "Author Name",
                        "description": "Description of the book"
                    }
                }
            }
        },
        400: {"description": "Invalid input"}
    }
)
def create_book(book: Book):
    """
    Create a new book.

    Args:
        book (Book): The book to create.

    Returns:
        Book: The created book.
    """
    book.id = str(uuid.uuid4())
    container.create_item(body=book.dict())
    return book

@app.get(
    "/books/",
    response_model=List[Book],
    responses={
        200: {
            "description": "A list of books",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "123",
                            "title": "Example Book",
                            "author": "Author Name",
                            "description": "Description of the book"
                        }
                    ]
                }
            }
        },
        400: {"description": "Invalid input"}
    }
)
def read_books(skip: int = 0, limit: int = 10):
    """
    Retrieve a list of books.

    Args:
        skip (int): Number of books to skip.
        limit (int): Maximum number of books to return.

    Returns:
        List[Book]: A list of books.
    """
    query = f"SELECT * FROM c OFFSET {skip} LIMIT {limit}"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return items

@app.get(
    "/books/{book_id}",
    response_model=Book,
    responses={
        200: {
            "description": "The retrieved book",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123",
                        "title": "Example Book",
                        "author": "Author Name",
                        "description": "Description of the book"
                    }
                }
            }
        },
        404: {"description": "Book not found"}
    }
)
def read_book(book_id: str):
    """
    Retrieve a book by its ID.

    Args:
        book_id (str): The ID of the book to retrieve.

    Returns:
        Book: The retrieved book.
    """
    try:
        item = container.read_item(item=book_id, partition_key=book_id)
        return item
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Book not found")

@app.put(
    "/books/{book_id}",
    response_model=Book,
    responses={
        200: {
            "description": "The updated book",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123",
                        "title": "Updated Book",
                        "author": "Author Name",
                        "description": "Updated description of the book"
                    }
                }
            }
        },
        404: {"description": "Book not found"},
        400: {"description": "Invalid input"}
    }
)
def update_book(book_id: str, updated_book: Book):
    """
    Update a book by its ID.

    Args:
        book_id (str): The ID of the book to update.
        updated_book (Book): The updated book data.

    Returns:
        Book: The updated book.
    """
    try:
        item = container.read_item(item=book_id, partition_key=book_id)
        updated_data = updated_book.dict(exclude_unset=True)
        item.update(updated_data)
        container.replace_item(item=book_id, body=item)
        return item
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Book not found")
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

@app.delete(
    "/books/{book_id}",
    response_model=Book,
    responses={
        200: {
            "description": "The deleted book",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123",
                        "title": "Deleted Book",
                        "author": "Author Name",
                        "description": "Description of the book"
                    }
                }
            }
        },
        404: {"description": "Book not found"}
    }
)
def delete_book(book_id: str):
    """
    Delete a book by its ID.

    Args:
        book_id (str): The ID of the book to delete.

    Returns:
        Book: The deleted book.
    """
    try:
        item = container.read_item(item=book_id, partition_key=book_id)
        container.delete_item(item=book_id, partition_key=book_id)
        return item
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Book not found")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )

# OpenTelemetry instrumentation
settings.tracing_implementation = "opentelemetry"
FastAPIInstrumentor.instrument_app(app)