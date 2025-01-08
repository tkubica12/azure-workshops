resource "azurerm_api_management_api_operation" "create_list" {
  operation_id        = "create-list"
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  display_name        = "Create List"
  method              = "POST"
  url_template        = "/lists/"
  description         = <<EOF
Create a new list.

Args:
    list (BooksList): The list to create.

Returns:
    BooksList: The created list.
EOF

  request {
    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.list.schema_id
      type_name    = "List"

      example {
        name  = "default"
        value = <<EOF
{
  "name": "Favorite Books",
  "description": "A list of my favorite books.",
  "books": ["Book One", "Book Two"]
}
EOF
      }
    }
  }

  response {
    status_code = 200
    description = "The created list"

    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.list.schema_id
      type_name    = "List"

      example {
        name  = "default"
        value = <<EOF
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Favorite Books",
  "description": "A list of my favorite books.",
  "books": ["Book One", "Book Two"]
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
      schema_id    = azurerm_api_management_api_schema.lists_validation_error.schema_id
      type_name    = "HTTPValidationError"

      example {
        name  = "default"
        value = <<EOF
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "Name is required",
      "type": "value_error"
    }
  ]
}
EOF
      }
    }
  }
}

resource "azurerm_api_management_api_operation_policy" "create_list" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  operation_id        = azurerm_api_management_api_operation.create_list.operation_id
  xml_content         = local.policy_lists
}

resource "azurerm_api_management_api_operation" "read_lists" {
  operation_id        = "read-lists"
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  display_name        = "Read Lists"
  method              = "GET"
  url_template        = "/lists/"
  description         = <<EOF
Retrieve a list of lists.

Args:
    skip (int): Number of lists to skip.
    limit (int): Maximum number of lists to return.

Returns:
    List[BooksList]: A list of lists.
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
    description = "A list of lists"

    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.lists.schema_id
      type_name    = "Lists"

      example {
        name  = "default"
        value = <<EOF
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Favorite Books",
    "description": "A list of my favorite books.",
    "books": ["Book One", "Book Two"]
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
      schema_id    = azurerm_api_management_api_schema.lists_validation_error.schema_id
      type_name    = "HTTPValidationError"

      example {
        name  = "default"
        value = <<EOF
{
  "detail": [
    {
      "loc": [],
      "msg": "Invalid query parameters",
      "type": "value_error"
    }
  ]
}
EOF
      }
    }
  }
}

resource "azurerm_api_management_api_operation_policy" "read_lists" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  operation_id        = azurerm_api_management_api_operation.read_lists.operation_id
  xml_content         = local.policy_lists
}

resource "azurerm_api_management_api_operation" "read_list" {
  operation_id        = "read-list"
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  display_name        = "Read List"
  method              = "GET"
  url_template        = "/lists/{list_id}"
  description         = <<EOF
Retrieve a list by its ID.

Args:
    list_id (str): The ID of the list to retrieve.

Returns:
    BooksList: The retrieved list.
EOF

  template_parameter {
    name          = "list_id"
    type          = "string"
    required      = true
    default_value = ""
  }

  response {
    status_code = 200
    description = "The retrieved list"

    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.list.schema_id
      type_name    = "List"

      example {
        name  = "default"
        value = <<EOF
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Favorite Books",
  "description": "A list of my favorite books.",
  "books": ["Book One", "Book Two"]
}
EOF
      }
    }
  }

  response {
    status_code = 404
    description = "List not found"
    representation {
      content_type = "application/json"
    }
  }

  response {
    status_code = 422
    description = "Validation Error"
    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.lists_validation_error.schema_id
      type_name    = "HTTPValidationError"

      example {
        name  = "default"
        value = <<EOF
{
  "detail": [
    {
      "loc": ["path", "list_id"],
      "msg": "Invalid list ID",
      "type": "value_error"
    }
  ]
}
EOF
      }
    }
  }
}

resource "azurerm_api_management_api_operation_policy" "read_list" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  operation_id        = azurerm_api_management_api_operation.read_list.operation_id
  xml_content         = local.policy_lists
}

resource "azurerm_api_management_api_operation" "update_list" {
  operation_id        = "update-list"
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  display_name        = "Update List"
  method              = "PUT"
  url_template        = "/lists/{list_id}"
  description         = <<EOF
Update a list by its ID.

Args:
    list_id (str): The ID of the list to update.
    updated_list (BooksList): The updated list data.

Returns:
    BooksList: The updated list.
EOF

  template_parameter {
    name          = "list_id"
    type          = "string"
    required      = true
    default_value = ""
  }

  request {
    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.list.schema_id
      type_name    = "List"

      example {
        name  = "default"
        value = <<EOF
{
  "name": "Updated List",
  "description": "An updated description.",
  "books": ["Book One", "Book Two", "Book Three"]
}
EOF
      }
    }
  }

  response {
    status_code = 200
    description = "The updated list"

    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.list.schema_id
      type_name    = "List"

      example {
        name  = "default"
        value = <<EOF
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Updated List",
  "description": "An updated description.",
  "books": ["Book One", "Book Two", "Book Three"]
}
EOF
      }
    }
  }

  response {
    status_code = 404
    description = "List not found"
    representation {
      content_type = "application/json"
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
      schema_id    = azurerm_api_management_api_schema.lists_validation_error.schema_id
      type_name    = "HTTPValidationError"

      example {
        name  = "default"
        value = <<EOF
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "Name is required",
      "type": "value_error"
    }
  ]
}
EOF
      }
    }
  }
}

resource "azurerm_api_management_api_operation_policy" "update_list" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  operation_id        = azurerm_api_management_api_operation.update_list.operation_id
  xml_content         = local.policy_lists
}

resource "azurerm_api_management_api_operation" "delete_list" {
  operation_id        = "delete-list"
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  display_name        = "Delete List"
  method              = "DELETE"
  url_template        = "/lists/{list_id}"
  description         = <<EOF
Delete a list by its ID.

Args:
    list_id (str): The ID of the list to delete.

Returns:
    BooksList: The deleted list.
EOF

  template_parameter {
    name          = "list_id"
    type          = "string"
    required      = true
    default_value = ""
  }

  response {
    status_code = 200
    description = "The deleted list"

    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.list.schema_id
      type_name    = "List"

      example {
        name  = "default"
        value = <<EOF
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Deleted List",
  "description": "This list has been deleted.",
  "books": ["Book One", "Book Two"]
}
EOF
      }
    }
  }

  response {
    status_code = 404
    description = "List not found"
    representation {
      content_type = "application/json"
    }
  }

  response {
    status_code = 422
    description = "Validation Error"
    representation {
      content_type = "application/json"
      schema_id    = azurerm_api_management_api_schema.lists_validation_error.schema_id
      type_name    = "HTTPValidationError"

      example {
        name  = "default"
        value = <<EOF
{
  "detail": [
    {
      "loc": ["path", "list_id"],
      "msg": "Invalid list ID",
      "type": "value_error"
    }
  ]
}
EOF
      }
    }
  }
}

resource "azurerm_api_management_api_operation_policy" "delete_list" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  operation_id        = azurerm_api_management_api_operation.delete_list.operation_id
  xml_content         = local.policy_lists
}

