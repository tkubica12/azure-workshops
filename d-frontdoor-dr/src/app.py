from flask import Flask, render_template, request, jsonify
import time
import os
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
# from opentelemetry import trace

app = Flask(__name__)

app_insights_connection_string = os.getenv('APP_INSIGHTS_CONNECTION_STRING')

configure_azure_monitor(connection_string=app_insights_connection_string)
FlaskInstrumentor().instrument_app(app)

@app.route('/')
def home():
    return render_template('index.html', app_insights_connection_string=app_insights_connection_string)

@app.route('/backend')
def backend():
    start_time = time.time()
    headers = dict(request.headers)
    latency = time.time() - start_time
    return jsonify(headers=headers, latency=latency)

@app.route('/health')
def health():
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True)