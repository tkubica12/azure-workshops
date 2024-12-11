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

app = FastAPI(title="Reviews", description="API to manage book reviews")
load_dotenv()

# Initialize CosmosDB client
credential = DefaultAzureCredential()
cosmos_endpoint = os.environ.get("COSMOSDB_ENDPOINT")
cosmos_client = CosmosClient(cosmos_endpoint, credential)
database_name = "BooksApp"
container_name = "Reviews"

# Create database and container if they don't exist
database = cosmos_client.create_database_if_not_exists(id=database_name)
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/id")
)

configure_azure_monitor()

@app.get("/", include_in_schema=False)
def get_openapi_spec():
    return app.openapi()

class Review(BaseModel):
    id: Optional[str] = None
    book_id: str
    review_text: str
    rating: int

@app.post(
    "/reviews/",
    response_model=Review,
    responses={
        200: {
            "description": "The created review",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "book_id": "book123",
                        "review_text": "Great book!",
                        "rating": 5
                    }
                }
            }
        },
        400: {"description": "Invalid input"}
    }
)
def create_review(review: Review):
    """
    Create a new review.

    Args:
        review (Review): The review to create.

    Returns:
        Review: The created review.
    """
    review.id = str(uuid.uuid4())
    container.create_item(body=review.dict())
    return review

@app.get(
    "/reviews/",
    response_model=List[Review],
    responses={
        200: {
            "description": "A list of reviews",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "book_id": "book123",
                            "review_text": "Great book!",
                            "rating": 5
                        }
                    ]
                }
            }
        },
        400: {"description": "Invalid input"}
    }
)
def read_reviews(skip: int = 0, limit: int = 10):
    """
    Retrieve a list of reviews.

    Args:
        skip (int): Number of reviews to skip.
        limit (int): Maximum number of reviews to return.

    Returns:
        List[Review]: A list of reviews.
    """
    query = f"SELECT * FROM c OFFSET {skip} LIMIT {limit}"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return items

@app.get(
    "/reviews/{review_id}",
    response_model=Review,
    responses={
        200: {
            "description": "The retrieved review",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "book_id": "book123",
                        "review_text": "Great book!",
                        "rating": 5
                    }
                }
            }
        },
        404: {"description": "Review not found"}
    }
)
def read_review(review_id: str):
    """
    Retrieve a review by its ID.

    Args:
        review_id (str): The ID of the review to retrieve.

    Returns:
        Review: The retrieved review.
    """
    try:
        item = container.read_item(item=review_id, partition_key=review_id)
        return item
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Review not found")

@app.put(
    "/reviews/{review_id}",
    response_model=Review,
    responses={
        200: {
            "description": "The updated review",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "book_id": "book123",
                        "review_text": "Updated review text.",
                        "rating": 4
                    }
                }
            }
        },
        404: {"description": "Review not found"},
        400: {"description": "Invalid input"}
    }
)
def update_review(review_id: str, updated_review: Review):
    """
    Update a review by its ID.

    Args:
        review_id (str): The ID of the review to update.
        updated_review (Review): The updated review data.

    Returns:
        Review: The updated review.
    """
    try:
        item = container.read_item(item=review_id, partition_key=review_id)
        updated_data = updated_review.dict(exclude_unset=True)
        item.update(updated_data)
        container.replace_item(item=review_id, body=item)
        return item
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Review not found")
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

@app.delete(
    "/reviews/{review_id}",
    response_model=Review,
    responses={
        200: {
            "description": "The deleted review",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "book_id": "book123",
                        "review_text": "This review has been deleted.",
                        "rating": 5
                    }
                }
            }
        },
        404: {"description": "Review not found"}
    }
)
def delete_review(review_id: str):
    """
    Delete a review by its ID.

    Args:
        review_id (str): The ID of the review to delete.

    Returns:
        Review: The deleted review.
    """
    try:
        item = container.read_item(item=review_id, partition_key=review_id)
        container.delete_item(item=review_id, partition_key=review_id)
        return item
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Review not found")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )

# OpenTelemetry instrumentation
settings.tracing_implementation = "opentelemetry"
FastAPIInstrumentor.instrument_app(app)