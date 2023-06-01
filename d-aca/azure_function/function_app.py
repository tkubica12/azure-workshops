import azure.functions as func
import logging
import time

app = func.FunctionApp()

@app.function_name(name="http_function")
@app.route(route="hello")
def http_function(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("HttpTrigger1 function processed a request!")

@app.function_name(name="queue_function")
@app.queue_trigger(arg_name="msg", queue_name="myqueue", connection="queueConnectionString")
def queue_function(msg: func.QueueMessage) -> None:
    logging.info('Python queue trigger function processed a queue item: %s', msg.get_body().decode('utf-8'))
    time.sleep(5)