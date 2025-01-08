import identity.web
import requests
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from dotenv import load_dotenv
import os
import json
from msal.oauth2cli.oidc import decode_id_token
from msal import ConfidentialClientApplication

# Configuration
load_dotenv()
config = {
    "REDIRECT_PATH": os.getenv("REDIRECT_PATH"),
    "AUTHORITY": os.getenv("AUTHORITY"),
    "MAIN_CLIENT_ID": os.getenv("MAIN_CLIENT_ID"),
    "MAIN_CLIENT_SECRET": os.getenv("MAIN_CLIENT_SECRET"),
    "BACKGROUND_CLIENT_ID": os.getenv("BACKGROUND_CLIENT_ID"),
    "BACKGROUND_CLIENT_SECRET": os.getenv("BACKGROUND_CLIENT_SECRET"),
    "ENTRA_SCOPES": json.loads(os.getenv("ENTRA_SCOPES")),
    "API_SCOPES": json.loads(os.getenv("API_SCOPES")),
    "API_SCOPES_CLIENT_CRED_FLOW": json.loads(os.getenv("API_SCOPES_CLIENT_CRED_FLOW")),
    "GRAPH_API_ENDPOINT": os.getenv("GRAPH_API_ENDPOINT"),
    "CUSTOM_API_ENDPOINT": os.getenv("CUSTOM_API_ENDPOINT"),
    "CUSTOM_API_APIM_PASSTHROUGH_ENDPOINT": os.getenv("CUSTOM_API_APIM_PASSTHROUGH_ENDPOINT"),
    "CUSTOM_API_APIM_REMOVEAUTH_ENDPOINT": os.getenv("CUSTOM_API_APIM_REMOVEAUTH_ENDPOINT"),
    "CUSTOM_API_APIM_ONBEHALF_ENDPOINT": os.getenv("CUSTOM_API_APIM_ONBEHALF_ENDPOINT"),
    "PAGE_NAME": os.getenv("PAGE_NAME"),
    "FLASK_SECRET_KEY": os.getenv('FLASK_SECRET_KEY')
}

app = Flask(__name__)
app.config['SECRET_KEY'] = config['FLASK_SECRET_KEY']
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Useful in template for B2C
app.jinja_env.globals.update(Auth=identity.web.Auth)
auth = identity.web.Auth(
    session=session,
    authority=config['AUTHORITY'],
    client_id=config['MAIN_CLIENT_ID'],
    client_credential=config['MAIN_CLIENT_SECRET'],
)

@app.route("/login")
def login():
    """Route to handle login."""
    return render_template("login.html", page_name=config['PAGE_NAME'], **auth.log_in(redirect_uri=url_for("auth_response", _external=True), prompt="select_account"))


@app.route("/graph_consent")
def graph_consent():
    """Route to handle consent for accessing Microsoft Graph."""
    return render_template("graph_consent.html", page_name=config['PAGE_NAME'], **auth.log_in(scopes=config['ENTRA_SCOPES'], redirect_uri=url_for("auth_response", _external=True), prompt="select_account"))

@app.route("/api_consent")
def api_consent():
    """Route to handle consent for accessing custom API."""
    return render_template("api_consent.html", page_name=config['PAGE_NAME'], **auth.log_in(scopes=config['API_SCOPES'], redirect_uri=url_for("auth_response", _external=True), prompt="select_account"))


@app.route(config['REDIRECT_PATH'])
def auth_response():
    """Route to handle the authentication response."""
    result = auth.complete_log_in(request.args)
    if "error" in result:
        return render_template("auth_error.html", result=result, page_name=config['PAGE_NAME'])
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    """Route to handle logout."""
    return redirect(auth.log_out(url_for("index", _external=True)))

@app.route("/")
def index():
    """Home page route."""
    if not auth.get_user():
        return redirect(url_for("login"))
    return render_template('index.html', token=auth.get_user(), page_name=config['PAGE_NAME'])


@app.route("/call_entra_graph")
def call_entra_graph():
    """Route to call Microsoft Graph API."""
    token = auth.get_token_for_user(config['ENTRA_SCOPES'])
    if "error" in token:
        if token.get("suberror") == "consent_required":
            return redirect(url_for("graph_consent"))
        else:
            return redirect(url_for("login"))

    api_result = requests.get(config['GRAPH_API_ENDPOINT'], headers={'Authorization': 'Bearer ' + token['access_token']}, timeout=30).json()
    decoded_token = decode_id_token(token['access_token'])
    return render_template('display.html', result=api_result, token=decoded_token, page_name=config['PAGE_NAME'])

@app.route("/custom_api")
def custom_api():
    """Route to call Custom API without any authorization."""
    response = requests.get(config['CUSTOM_API_ENDPOINT'])
    if response.status_code == 401:
        # If the API returns a 401 status, render the unauthorized page
        return render_template('unauthorized.html', page_name=config['PAGE_NAME'])
    else:
        # Otherwise, proceed as normal
        api_result = response.json()
        return render_template('display.html', result=api_result, token="", page_name=config['PAGE_NAME'])
    
@app.route("/custom_api_user")
def custom_api_user():
    """Route to call Custom API using user token."""
    token = auth.get_token_for_user(config['API_SCOPES'])
    if "error" in token:
        if token.get("suberror") == "consent_required":
            return redirect(url_for("api_consent"))
        else:
            return redirect(url_for("login"))
        
    response = requests.get(config['CUSTOM_API_ENDPOINT'], headers={'Authorization': 'Bearer ' + token['access_token']})
    if response.status_code == 401:
        # If the API returns a 401 status, render the unauthorized page
        return render_template('unauthorized.html', page_name=config['PAGE_NAME'])
    else:
        # Otherwise, proceed as normal
        api_result = response.json()
        decoded_token = decode_id_token(token['access_token'])
        return render_template('display.html', result=api_result, token=decoded_token, page_name=config['PAGE_NAME'])
    
@app.route("/custom_api_service")
def custom_api_service():
    """Route to call Custom API using service token."""
    client_app = ConfidentialClientApplication(
        client_id=config['BACKGROUND_CLIENT_ID'],
        authority=config['AUTHORITY'],
        client_credential=config['BACKGROUND_CLIENT_SECRET'],
    )

    token = client_app.acquire_token_for_client(scopes=config['API_SCOPES_CLIENT_CRED_FLOW'])

    if "access_token" in token:
        # Use the access token to call the Custom API
        response = requests.get(config['CUSTOM_API_ENDPOINT'], headers={'Authorization': 'Bearer ' + token['access_token']})
        if response.status_code == 401:
            return render_template('unauthorized.html', page_name=config['PAGE_NAME'])
        else:
            api_result = response.json()
            decoded_token = decode_id_token(token['access_token'])
            return render_template('display.html', result=api_result, token=decoded_token, page_name=config['PAGE_NAME'])
    else:
        return render_template('service_error.html', error="Cannot acquire token for service", page_name=config['PAGE_NAME'])
    
@app.route("/custom_api_apim_passthrough")
def custom_api_apim_passthrough():
    """Route to call Custom API via APIM using user token."""
    token = auth.get_token_for_user(config['API_SCOPES'])
    if "error" in token:
        if token.get("suberror") == "consent_required":
            return redirect(url_for("api_consent"))
        else:
            return redirect(url_for("login"))
        
    response = requests.get(config['CUSTOM_API_APIM_PASSTHROUGH_ENDPOINT'], headers={'Authorization': 'Bearer ' + token['access_token']})
    if response.status_code == 401:
        # If the API returns a 401 status, render the unauthorized page
        print(response.text)
        return render_template('unauthorized.html', page_name=config['PAGE_NAME'])
    else:
        # Otherwise, proceed as normal
        api_result = response.json()
        decoded_token = decode_id_token(token['access_token'])
        return render_template('display.html', result=api_result, token=decoded_token, page_name=config['PAGE_NAME'])

    
@app.route("/custom_api_apim_removeauth")
def custom_api_apim_removeauth():
    """Route to call Custom API on APIM using service token, APIM terminates and send plain to API."""
    client_app = ConfidentialClientApplication(
        client_id=config['BACKGROUND_CLIENT_ID'],
        authority=config['AUTHORITY'],
        client_credential=config['BACKGROUND_CLIENT_SECRET'],
    )

    token = client_app.acquire_token_for_client(scopes=config['API_SCOPES_CLIENT_CRED_FLOW'])

    if "access_token" in token:
        # Use the access token to call the Custom API
        response = requests.get(config['CUSTOM_API_APIM_REMOVEAUTH_ENDPOINT'], headers={'Authorization': 'Bearer ' + token['access_token']})
        if response.status_code == 401:
            print(response.text)
            return render_template('unauthorized.html', page_name=config['PAGE_NAME'])
        else:
            api_result = response.json()
            decoded_token = decode_id_token(token['access_token'])
            return render_template('display.html', result=api_result, token=decoded_token, page_name=config['PAGE_NAME'])
    else:
        return render_template('service_error.html', error="Cannot acquire token for service", page_name=config['PAGE_NAME'])
    
@app.route("/custom_api_apim_onbehalf")
def custom_api_apim_onbehalf():
    """Route to call Custom API on APIM without any authorization."""
    response = requests.get(config['CUSTOM_API_APIM_ONBEHALF_ENDPOINT'])
    if response.status_code == 401:
        # If the API returns a 401 status, render the unauthorized page
        print(response.text)
        return render_template('unauthorized.html', page_name=config['PAGE_NAME'])
    else:
        # Otherwise, proceed as normal
        api_result = response.json()
        return render_template('display.html', result=api_result, token="", page_name=config['PAGE_NAME'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)