resource "azurerm_api_management_api_schema" "review" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  schema_id           = "review"
  content_type        = "application/vnd.ms-azure-apim.swagger+json"
  value               = <<JSON
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Review",
  "type": "object",
  "required": ["book_id", "review_text", "rating"],
  "properties": {
    "id": {
      "title": "Id",
      "type": ["string", "null"]
    },
    "book_id": {
      "title": "Book Id",
      "type": "string"
    },
    "review_text": {
      "title": "Review Text",
      "type": "string"
    },
    "rating": {
      "title": "Rating",
      "type": "integer"
    }
  }
}
JSON
}

resource "azurerm_api_management_api_schema" "reviews_validation_error" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  schema_id           = "reviews_ValidationError"
  content_type        = "application/vnd.ms-azure-apim.swagger+json"
  value               = <<JSON
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ValidationError",
  "type": "object",
  "required": ["loc", "msg", "type"],
  "properties": {
    "loc": {
      "title": "Location",
      "type": "array",
      "items": {
        "anyOf": [
          { "type": "string" },
          { "type": "integer" }
        ]
      }
    },
    "msg": {
      "title": "Message",
      "type": "string"
    },
    "type": {
      "title": "Error Type",
      "type": "string"
    }
  }
}
JSON
}

resource "azurerm_api_management_api_schema" "reviews_http_validation_error" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  schema_id           = "reviews_HTTPValidationError"
  content_type        = "application/vnd.ms-azure-apim.swagger+json"
  value               = <<JSON
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "HTTPValidationError",
  "type": "object",
  "properties": {
    "detail": {
      "title": "Detail",
      "type": "array",
      "items": {
        "$ref": "#/definitions/ValidationError"
      }
    }
  },
  "definitions": {
    "ValidationError": {
      "title": "ValidationError",
      "type": "object",
      "required": ["loc", "msg", "type"],
      "properties": {
        "loc": {
          "title": "Location",
          "type": "array",
          "items": {
            "anyOf": [
              { "type": "string" },
              { "type": "integer" }
            ]
          }
        },
        "msg": {
          "title": "Message",
          "type": "string"
        },
        "type": {
          "title": "Error Type",
          "type": "string"
        }
      }
    }
  }
}
JSON
}

# ...existing code...
