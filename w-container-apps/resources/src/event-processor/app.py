from cloudevents.sdk.event import v1
from dapr.ext.grpc import App
import json

app = App()

# Default subscription for a topic
@app.subscribe(pubsub_name='pubsub', topic='DEMO')
def mytopic(event: v1.Event) -> None:
    data = json.loads(event.Data())
    print(f'Received: id={data["id"]}, message="{data ["message"]}"' ,flush=True)

app.run(5001)