config = {
    "env_file_path": ".env",
    "applications": {
        "main": {
            "display_name": "tokubica-auth-entra-web",
            "redirect_uris": ["http://localhost:5000/auth_response"]
        },
        "api": {
            "display_name": "tokubica-auth-entra-api",
            "redirect_uris": ["http://localhost:5001/auth_response"],
            "permission_scopes": {
                "read": {
                    "id": "74af35a7-6c8e-4051-9b15-86164a12bec5"
                },
                "write": {
                    "id": "999f35a7-6c8e-4051-9b15-86164a12bec5"
                }
            }
        },
        "apim": {
            "display_name": "tokubica-auth-entra-apim"
            # No redirect URIs
        },
        "background": {
            "display_name": "tokubica-auth-entra-background"
        }
    }
}