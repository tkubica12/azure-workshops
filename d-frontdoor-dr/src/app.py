# Import necessary modules
from flask import Flask, render_template, request, jsonify
import time
import os
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
import logging

# Set up basic logging configuration
logging.basicConfig(format = "%(asctime)s:%(levelname)s:%(message)s", level = logging.ERROR)

# Create a logger object
logger = logging.getLogger(__name__)
stream = logging.StreamHandler()
logger.addHandler(stream)

# Create a Flask app
app = Flask(__name__)

# Get the Application Insights connection string from environment variable
app_insights_connection_string = os.getenv('APP_INSIGHTS_CONNECTION_STRING')

# Configure Azure Monitor with the connection string
configure_azure_monitor(connection_string=app_insights_connection_string)

# Instrument the Flask app for telemetry data
FlaskInstrumentor().instrument_app(app)

# Define the route for the home page
@app.route('/')
def home():
    # Render the home page with the connection string
    return render_template('index.html', app_insights_connection_string=app_insights_connection_string)

# Define the route for the backend
@app.route('/backend')
def backend():
    # Get the request headers
    headers = dict(request.headers)

    # Return the headers and latency as JSON
    return jsonify(headers=headers)

# Define the route for the health check
@app.route('/health')
def health():
    # Return a simple OK message
    return 'OK'

# Run the app
if __name__ == '__main__':
    app.run(debug=False)