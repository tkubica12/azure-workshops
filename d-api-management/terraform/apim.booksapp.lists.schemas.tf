resource "azurerm_api_management_api_schema" "lists" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  schema_id           = "lists"
  content_type        = "application/vnd.ms-azure-apim.swagger+json"
  value               = <<JSON
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "array",
  "items": {
    "$ref": "#/definitions/list"
  },
  "definitions": {
    "list": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "description": { "type": ["string", "null"] },
        "books": {
          "type": "array",
          "items": { "type": "string" },
          "default": []
        }
      },
      "required": ["name"]
    }
  }
}
JSON
}

resource "azurerm_api_management_api_schema" "list" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  schema_id           = "list"
  content_type        = "application/vnd.ms-azure-apim.swagger+json"
  value               = <<JSON
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "id": { "type": "string" },
    "name": { "type": "string" },
    "description": { "type": ["string", "null"] },
    "books": {
      "type": "array",
      "items": { "type": "string" },
      "default": []
    }
  },
  "required": ["name"]
}
JSON
}

resource "azurerm_api_management_api_schema" "lists_validation_error" {
  api_name            = azurerm_api_management_api.booksapp.name
  api_management_name = azurerm_api_management.main.name
  resource_group_name = azurerm_resource_group.main.name
  schema_id           = "lists_validation_error"
  content_type        = "application/vnd.ms-azure-apim.swagger+json"
  value               = <<JSON
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "detail": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/validationerror"
      }
    }
  },
  "definitions": {
    "validationerror": {
      "type": "object",
      "properties": {
        "loc": {
          "type": "array",
          "items": { "type": ["string", "integer"] }
        },
        "msg": { "type": "string" },
        "type": { "type": "string" }
      },
      "required": ["loc", "msg", "type"]
    }
  },
  "required": ["detail"]
}
JSON
}

