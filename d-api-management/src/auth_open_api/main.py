from flask import Flask, jsonify, request, abort
import msal
from dotenv import load_dotenv
import os
import jwt
import time
import requests
import base64

app = Flask(__name__)

@app.route("/")
def api():
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
