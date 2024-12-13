resource "azurerm_api_management_api_operation" "create_review" {
  operation_id        = "create-review"
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  display_name        = "Create Review"
  method              = "POST"
  url_template        = "/reviews/"
  description         = <<EOF
Create a new review.

Args:
    review (Review): The review to create.

Returns:
    Review: The created review.
EOF

  request {
    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.review.schema_id
      type_name    = "Review"

      example {
        name  = "default"
        value = <<EOF
{
  "book_id": "book123",
  "review_text": "Great book!",
  "rating": 5
}
EOF
      }
    }
  }

  response {
    status_code = 200
    description = "The created review"

    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.review.schema_id
      type_name    = "Review"

      example {
        name  = "default"
        value = <<EOF
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "book_id": "book123",
  "review_text": "Great book!",
  "rating": 5
}
EOF
      }
    }
  }

  response {
    status_code = 400
    description = "Invalid input"
    representation {
      content_type = "application/json"
    }
  }

  response {
    status_code = 422
    description = "Validation Error"
    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.reviews_http_validation_error.schema_id
      type_name    = "HTTPValidationError"
    }
  }
}

resource "azurerm_api_management_api_operation" "read_reviews" {
  operation_id        = "read-reviews"
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  display_name        = "Read Reviews"
  method              = "GET"
  url_template        = "/reviews/"
  description         = <<EOF
Retrieve a list of reviews.

Args:
    skip (int): Number of reviews to skip.
    limit (int): Maximum number of reviews to return.

Returns:
    List[Review]: A list of reviews.
EOF

  request {
    query_parameter {
      name          = "skip"
      type          = "integer"
      default_value = "0"
      required      = false
    }
    query_parameter {
      name          = "limit"
      type          = "integer"
      default_value = "10"
      required      = false
    }
  }

  response {
    status_code = 200
    description = "A list of reviews"

    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.review.schema_id
      type_name    = "Review[]"

      example {
        name  = "default"
        value = <<EOF
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "book_id": "book123",
    "review_text": "Great book!",
    "rating": 5
  }
]
EOF
      }
    }
  }

  response {
    status_code = 400
    description = "Invalid input"
    representation {
      content_type = "application/json"
    }
  }

  response {
    status_code = 422
    description = "Validation Error"
    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.reviews_http_validation_error.schema_id
      type_name    = "HTTPValidationError"
    }
  }
}

resource "azurerm_api_management_api_operation" "read_review" {
  operation_id        = "read-review"
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  display_name        = "Read Review"
  method              = "GET"
  url_template        = "/reviews/{review_id}"
  description         = <<EOF
Retrieve a review by its ID.

Args:
    review_id (str): The ID of the review to retrieve.

Returns:
    Review: The retrieved review.
EOF

  template_parameter {
    name          = "review_id"
    type          = "string"
    required      = true
    default_value = ""
  }

  response {
    status_code = 200
    description = "The retrieved review"

    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.review.schema_id
      type_name    = "Review"

      example {
        name  = "default"
        value = <<EOF
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "book_id": "book123",
  "review_text": "Great book!",
  "rating": 5
}
EOF
      }
    }
  }

  response {
    status_code = 404
    description = "Review not found"
    representation {
      content_type = "application/json"
    }
  }

  response {
    status_code = 422
    description = "Validation Error"
    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.reviews_http_validation_error.schema_id
      type_name    = "HTTPValidationError"
    }
  }
}

resource "azurerm_api_management_api_operation" "update_review" {
  operation_id        = "update-review"
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  display_name        = "Update Review"
  method              = "PUT"
  url_template        = "/reviews/{review_id}"
  description         = <<EOF
Update a review by its ID.

Args:
    review_id (str): The ID of the review to update.
    updated_review (Review): The updated review data.

Returns:
    Review: The updated review.
EOF

  template_parameter {
    name          = "review_id"
    type          = "string"
    required      = true
    default_value = ""
  }

  request {
    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.review.schema_id
      type_name    = "Review"

      example {
        name  = "default"
        value = <<EOF
{
  "book_id": "book123",
  "review_text": "Updated review text.",
  "rating": 4
}
EOF
      }
    }
  }

  response {
    status_code = 200
    description = "The updated review"

    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.review.schema_id
      type_name    = "Review"

      example {
        name  = "default"
        value = <<EOF
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "book_id": "book123",
  "review_text": "Updated review text.",
  "rating": 4
}
EOF
      }
    }
  }

  response {
    status_code = 400
    description = "Invalid input"
    representation {
      content_type = "application/json"
    }
  }

  response {
    status_code = 404
    description = "Review not found"
    representation {
      content_type = "application/json"
    }
  }

  response {
    status_code = 422
    description = "Validation Error"
    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.reviews_http_validation_error.schema_id
      type_name    = "HTTPValidationError"
    }
  }
}

resource "azurerm_api_management_api_operation" "delete_review" {
  operation_id        = "delete-review"
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  display_name        = "Delete Review"
  method              = "DELETE"
  url_template        = "/reviews/{review_id}"
  description         = <<EOF
Delete a review by its ID.

Args:
    review_id (str): The ID of the review to delete.

Returns:
    Review: The deleted review.
EOF

  template_parameter {
    name          = "review_id"
    type          = "string"
    required      = true
    default_value = ""
  }

  response {
    status_code = 200
    description = "The deleted review"

    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.review.schema_id
      type_name    = "Review"

      example {
        name  = "default"
        value = <<EOF
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "book_id": "book123",
  "review_text": "This review has been deleted.",
  "rating": 5
}
EOF
      }
    }
  }

  response {
    status_code = 404
    description = "Review not found"
    representation {
      content_type = "application/json"
    }
  }

  response {
    status_code = 422
    description = "Validation Error"
    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.reviews_http_validation_error.schema_id
      type_name    = "HTTPValidationError"
    }
  }
}

# ...existing code...
