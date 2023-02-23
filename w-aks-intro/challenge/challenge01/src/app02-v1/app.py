# Simple Python Flask web app
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<H1>Hello from Python v1!</H1>"

app.run(host='0.0.0.0', port=8080)