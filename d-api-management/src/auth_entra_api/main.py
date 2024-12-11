from flask import Flask, jsonify, request, abort
import msal
from dotenv import load_dotenv
import os
import jwt
import time
import requests
import base64
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Configuration
load_dotenv()
config = {
    "API_CLIENT_ID": os.getenv("API_CLIENT_ID"),
    "API_CLIENT_SECRET": os.getenv("API_CLIENT_SECRET"),
    "AUTHORITY": os.getenv("AUTHORITY"),
    "SCOPES": ["Stuff.Read"],
}

app = Flask(__name__)

# Get well-known configuration OIDC to find jwks uri
oid_config = requests.get(
    f"{config['AUTHORITY']}/v2.0/.well-known/openid-configuration").json()
jwks_uri = oid_config["jwks_uri"]
issuer = oid_config["issuer"]

# Get jwks keys and store it as dictionary
jwks = requests.get(jwks_uri).json()
rsa_keys = {}
for key in jwks["keys"]:
    rsa_key = {
        "kty": key["kty"],
        "kid": key["kid"],
        "use": key["use"],
        "n": key["n"],
        "e": key["e"]
    }
    rsa_keys[key["kid"]] = jwt.algorithms.RSAAlgorithm.from_jwk(rsa_key)


def validate_token(auth_header):
    token = auth_header.split(' ')[1]
    unverified_header = jwt.get_unverified_header(token)
    print(f"Received token with header: {unverified_header}")
    decoded_token = None
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": True}, algorithms=[
                                   "RS256"], key=rsa_keys[unverified_header['kid']], audience=config['API_CLIENT_ID'], issuer=issuer)

    except jwt.PyJWTError as e:
        print(f"Token validation error: {e}")
        return None

    return decoded_token


@app.route("/")
def api():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        abort(401)  # Unauthorized if no auth header

    token_validation_result = validate_token(auth_header)
    if not token_validation_result:
        abort(401)  # Unauthorized if token is invalid

    data = {
        "message": "Hello!",
        "status": "success",
        "data": {
            "name": "John Doe",
            "age": 30,
        }
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
