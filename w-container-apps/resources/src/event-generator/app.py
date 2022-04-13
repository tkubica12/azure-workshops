from dapr.clients import DaprClient
from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
def web():
   return '''
   <script>
   const userAction = async () => {
        const response = await fetch('/api/messages', {
            method: 'POST',
            body: '', 
            headers: {
            'Content-Type': 'application/json'
            }
        });
        const myJson = await response.json();
        }
    </script>
    <button onclick="userAction()">Send message</button>
    '''

@app.route('/api/messages', methods=['POST'])
def send_message():
    with DaprClient() as d:
        mydata = {
            'id': 0,
            'message': 'hello world'
        }
        resp = d.publish_event(pubsub_name='pubsub', topic_name='DEMO', data=json.dumps(mydata),data_content_type='application/json')
    return 'ok'

if __name__ == '__main__':
   app.run()