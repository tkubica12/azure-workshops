resource "azurerm_api_management_api_schema" "books" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  schema_id           = "books"
  content_type        = "application/vnd.ms-azure-apim.swagger+json"
  value               = <<JSON
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "id": {
        "type": "string"
      },
      "title": {
        "type": "string"
      },
      "author": {
        "type": "string"
      },
      "description": {
        "type": "string"
      }
    },
    "required": ["id", "title", "author", "description"]
  }
}
JSON
}

resource "azurerm_api_management_api_schema" "book" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  schema_id           = "book"
  content_type        = "application/vnd.ms-azure-apim.swagger+json"
  value               = <<JSON
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "id": {
      "type": "string"
    },
    "title": {
      "type": "string"
    },
    "author": {
      "type": "string"
    },
    "description": {
      "type": "string"
    }
  },
  "required": ["id", "title", "author", "description"]
}
JSON
}

resource "azurerm_api_management_api_schema" "books_validation_error" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  schema_id           = "books_validation_error"
  content_type        = "application/vnd.ms-azure-apim.swagger+json"
  value               = <<JSON
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "detail": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "loc": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "msg": {
            "type": "string"
          },
          "type": {
            "type": "string"
          }
        },
        "required": ["loc", "msg", "type"]
      }
    }
  },
  "required": ["detail"]
}
JSON
}

resource "azurerm_api_management_api_schema" "books_get_request" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  schema_id           = "books_get_request"
  content_type        = "application/vnd.ms-azure-apim.swagger+json"
  value               = <<JSON
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "skip": {
      "type": "integer",
      "default": 0
    },
    "limit": {
      "type": "integer",
      "default": 10
    }
  },
  "required": ["skip", "limit"]
}
JSON
}

resource "azurerm_api_management_api_schema" "books_book_id_get_request" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  schema_id           = "books_book_id_get_request"
  content_type        = "application/vnd.ms-azure-apim.swagger+json"
  value               = <<JSON
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "book_id": {
      "type": "string",
      "default": ""
    }
  },
  "required": ["book_id"]
}
JSON
}

resource "azurerm_api_management_api_schema" "book_update_request" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  schema_id           = "book_update_request"
  content_type        = "application/vnd.ms-azure-apim.swagger+json"
  value               = <<JSON
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "title": {
      "type": "string"
    },
    "author": {
      "type": "string"
    },
    "description": {
      "type": "string"
    }
  },
  "required": ["title", "author", "description"]
}
JSON
}

resource "azurerm_api_management_api_schema" "book_update_response" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  schema_id           = "book_update_response"
  content_type        = "application/vnd.ms-azure-apim.swagger+json"
  value               = <<JSON
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "id": {
      "type": "string"
    },
    "title": {
      "type": "string"
    },
    "author": {
      "type": "string"
    },
    "description": {
      "type": "string"
    }
  },
  "required": ["id", "title", "author", "description"]
}
JSON
}

resource "azurerm_api_management_api_schema" "book_create_request" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  schema_id           = "book_create_request"
  content_type        = "application/vnd.ms-azure-apim.swagger+json"
  value               = <<JSON
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "title": {
      "type": "string"
    },
    "author": {
      "type": "string"
    },
    "description": {
      "type": "string"
    }
  },
  "required": ["title", "author", "description"]
}
JSON
}

resource "azurerm_api_management_api_schema" "book_create_response" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  schema_id           = "book_create_response"
  content_type        = "application/vnd.ms-azure-apim.swagger+json"
  value               = <<JSON
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "id": {
      "type": "string"
    },
    "title": {
      "type": "string"
    },
    "author": {
      "type": "string"
    },
    "description": {
      "type": "string"
    }
  },
  "required": ["id", "title", "author", "description"]
}
JSON
}

