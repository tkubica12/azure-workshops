resource "azurerm_api_management_api_operation" "read_books" {
  operation_id        = "read-books"
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  display_name        = "Read Books"
  method              = "GET"
  url_template        = "/books/"
  description         = <<EOF
Retrieve a list of books.

Args:
    skip (int): Number of books to skip.
    limit (int): Maximum number of books to return.

Returns:
    List[Book]: A list of books.
EOF

  request {
    query_parameter {
      name          = "skip"
      type          = "integer"
      default_value = "0"
      values        = []
      schema_id     = azurerm_api_management_api_schema.books_get_request.schema_id
      required      = false
    }
    query_parameter {
      name          = "limit"
      type          = "integer"
      default_value = "10"
      values        = []
      schema_id     = azurerm_api_management_api_schema.books_get_request.schema_id
      required      = false
    }
  }

  response {
    status_code = 200
    description = "A list of books"

    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.books.schema_id

      example {
        name  = "default"
        value = <<EOF
[{"id":"123","title":"Example Book","author":"Author Name","description":"Description of the book"}]
EOF
      }
    }
  }

  response {
    status_code = 404
    description = "Book not found"
    representation {
      content_type = "application/json"
      example {
        name  = "default"
        value = "[]"
      }
    }
  }

  response {
    status_code = 400
    description = "Invalid input"
    representation {
      content_type = "application/json"
      example {
        name  = "default"
        value = "[]"
      }
    }
  }

  response {
    status_code = 422
    description = "Validation Error"
    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.books_validation_error.schema_id
      example {
        name  = "default"
        value = <<EOF
{
  "detail": [
    {
      "loc": [],
      "msg": "string",
      "type": "string"
    }
  ]
}
EOF
      }
    }
  }
}

resource "azurerm_api_management_api_operation_policy" "read_books" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  operation_id        = azurerm_api_management_api_operation.read_books.operation_id
  xml_content         = local.policy_books
}


resource "azurerm_api_management_api_operation" "read_book" {
  operation_id        = "read-book"
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  display_name        = "Read Book"
  method              = "GET"
  url_template        = "/books/{book_id}"
  description         = <<EOF
Retrieve a book by its ID.

Args:
    book_id (str): The ID of the book to retrieve.

Returns:
    Book: The retrieved book.
EOF

  template_parameter {
    name         = "book_id"
    type         = "string"
    required     = true
    schema_id    = azurerm_api_management_api_schema.books_book_id_get_request.schema_id
    type_name    = "Books-book_id-GetRequest"
    default_value = ""
    values       = []
  }

  response {
    status_code = 200
    description = "The retrieved book"

    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.book.schema_id

      example {
        name  = "default"
        value = <<EOF
{
  "id": "123",
  "title": "Example Book",
  "author": "Author Name",
  "description": "Description of the book"
}
EOF
      }
    }
  }

  response {
    status_code = 404
    description = "Book not found"
    representation {
      content_type = "application/json"
      example {
        name  = "default"
        value = <<EOF
{
  "detail": [
    {
      "loc": [],
      "msg": "Book not found",
      "type": "not_found"
    }
  ]
}
EOF
      }
    }
  }

  response {
    status_code = 422
    description = "Validation Error"
    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.books_validation_error.schema_id

      example {
        name  = "default"
        value = <<EOF
{
  "detail": [
    {
      "loc": ["path", "book_id"],
      "msg": "Invalid book ID",
      "type": "value_error"
    }
  ]
}
EOF
      }
    }
  }
}

resource "azurerm_api_management_api_operation_policy" "read_book" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  operation_id        = azurerm_api_management_api_operation.read_book.operation_id
  xml_content         = local.policy_books
}

resource "azurerm_api_management_api_operation" "update_book" {
  operation_id        = "update-book"
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  display_name        = "Update Book"
  method              = "PUT"
  url_template        = "/books/{book_id}"
  description         = <<EOF
Update a book by its ID.

Args:
    book_id (str): The ID of the book to update.
    updated_book (Book): The updated book data.

Returns:
    Book: The updated book.
EOF

  template_parameter {
    name          = "book_id"
    type          = "string"
    required      = true
    schema_id     = azurerm_api_management_api_schema.books_book_id_get_request.schema_id
    type_name     = "Books-book_id-PutRequest"
    default_value = ""
    values        = []
  }

  request {
    representation {
      content_type = "application/json"
      example {
        name  = "default"
        value = <<EOF
{
  "title": "string",
  "author": "string",
  "description": "string"
}
EOF
      }
      schema_id = azurerm_api_management_api_schema.book_update_request.schema_id
      type_name = "BookUpdateRequest"
    }
  }

  response {
    status_code = 200
    description = "The updated book"

    representation {
      content_type = "application/json"
      example {
        name  = "default"
        value = <<EOF
{
  "id": "123",
  "title": "Updated Book",
  "author": "Author Name",
  "description": "Updated description of the book"
}
EOF
      }
      schema_id = azurerm_api_management_api_schema.book_update_response.schema_id
      type_name = "Book"
    }
  }

  response {
    status_code = 404
    description = "Book not found"
    representation {
      content_type = "application/json"
      example {
        name  = "default"
        value = <<EOF
[]
EOF
      }
    }
  }

  response {
    status_code = 400
    description = "Invalid input"
    representation {
      content_type = "application/json"
      example {
        name  = "default"
        value = <<EOF
[]
EOF
      }
    }
  }

  response {
    status_code = 422
    description = "Validation Error"
    representation {
      content_type = "application/json"
      example {
        name  = "default"
        value = <<EOF
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Title is required",
      "type": "value_error"
    }
  ]
}
EOF
      }
      schema_id = azurerm_api_management_api_schema.books_validation_error.schema_id
      type_name = "HTTPValidationError"
    }
  }
}

resource "azurerm_api_management_api_operation_policy" "update_book" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  operation_id        = azurerm_api_management_api_operation.update_book.operation_id
  xml_content         = local.policy_books
}

resource "azurerm_api_management_api_operation" "create_book" {
  operation_id        = "create-book"
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  display_name        = "Create Book"
  method              = "POST"
  url_template        = "/books/"
  description         = <<EOF
Create a new book.

Args:
    book (Book): The book to create.

Returns:
    Book: The created book.
EOF

  request {
    representation {
      content_type = "application/json"
      example {
        name  = "default"
        value = <<EOF
{
  "title": "string",
  "author": "string",
  "description": "string"
}
EOF
      }
      schema_id = azurerm_api_management_api_schema.book_create_request.schema_id
      type_name = "BookCreateRequest"
    }
  }

  response {
    status_code = 200
    description = "The created book"

    representation {
      content_type = "application/json"
      example {
        name  = "default"
        value = <<EOF
{
  "id": "123",
  "title": "Example Book",
  "author": "Author Name",
  "description": "Description of the book"
}
EOF
      }
      schema_id = azurerm_api_management_api_schema.book_create_response.schema_id
      type_name = "Book"
    }
  }

  response {
    status_code = 400
    description = "Invalid input"
    representation {
      content_type = "application/json"
      example {
        name  = "default"
        value = <<EOF
[]
EOF
      }
    }
  }

  response {
    status_code = 422
    description = "Validation Error"
    representation {
      content_type = "application/json"
      example {
        name  = "default"
        value = <<EOF
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Title is required",
      "type": "value_error"
    }
  ]
}
EOF
      }
      schema_id = azurerm_api_management_api_schema.books_validation_error.schema_id
      type_name = "HTTPValidationError"
    }
  }
}

resource "azurerm_api_management_api_operation_policy" "create_book" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  operation_id        = azurerm_api_management_api_operation.create_book.operation_id
  xml_content         = local.policy_books
}

resource "azurerm_api_management_api_operation" "delete_book" {
  operation_id        = "delete-book"
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  display_name        = "Delete Book"
  method              = "DELETE"
  url_template        = "/books/{book_id}"
  description         = <<EOF
Delete a book by its ID.

Args:
    book_id (str): The ID of the book to delete.

Returns:
    Book: The deleted book.
EOF

  template_parameter {
    name          = "book_id"
    type          = "string"
    required      = true
    schema_id     = azurerm_api_management_api_schema.books_book_id_get_request.schema_id
    type_name     = "Books-book_id-DeleteRequest"
    default_value = ""
    values        = []
  }


  response {
    status_code = 200
    description = "The deleted book"

    representation {
      content_type = "application/json"
      example {
        name  = "default"
        value = <<EOF
{
  "id": "123",
  "title": "Deleted Book",
  "author": "Author Name",
  "description": "Description of the book"
}
EOF
      }
      schema_id = azurerm_api_management_api_schema.book.schema_id
      type_name = "Book"
    }
  }

  response {
    status_code = 404
    description = "Book not found"
    representation {
      content_type = "application/json"
      example {
        name  = "default"
        value = <<EOF
[]
EOF
      }
    }
  }

  response {
    status_code = 422
    description = "Validation Error"
    representation {
      content_type = "application/json"
      example {
        name  = "default"
        value = <<EOF
{
  "detail": [
    {
      "loc": ["body", "book_id"],
      "msg": "Invalid book ID",
      "type": "value_error"
    }
  ]
}
EOF
      }
      schema_id = azurerm_api_management_api_schema.books_validation_error.schema_id
      type_name = "HTTPValidationError"
    }
  }
}

resource "azurerm_api_management_api_operation_policy" "delete_book" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  operation_id        = azurerm_api_management_api_operation.delete_book.operation_id
  xml_content         = local.policy_books
}

