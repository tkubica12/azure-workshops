import os
import uuid
import time
import json
from locust import HttpUser, task, between, events
from dotenv import load_dotenv
import sseclient

load_dotenv()

LOCUST_HOST = os.getenv("LOCUST_HOST", "http://localhost:8000")
DEFAULT_TEST_MESSAGE = "Hello from Locust test user"
TEST_MESSAGE = os.getenv("TEST_MESSAGE", DEFAULT_TEST_MESSAGE)

sse_stats: dict[str, dict[str, float]] = {}

@events.test_stop.add_listener
def display_custom_stats(environment, **kwargs):
    """
    Print custom SSE stats summary at the end of the test run.
    """
    print("\n----------------------------------------------------\nCustom SSE stats summary:")
    for name, metrics in sse_stats.items():
        print(f"\nStats for {name}:")
        for k, v in metrics.items():
            print(f"  {k}: {v}")
    print("\n----------------------------------------------------\n")

class ChatUser(HttpUser):
    """
    Simulates a chat user that starts a session and sends chat messages, processing SSE streams.
    """
    wait_time = between(1, 5)

    def on_start(self):
        """
        Initialize user session and set base URL.
        """
        self.session_id = None
        self.client.base_url = LOCUST_HOST
        self.start_chat_session()

    def start_chat_session(self):
        """
        Starts a new chat session and stores the session ID.
        """
        try:
            response = self.client.post("/api/session/start")
            response.raise_for_status()
            self.session_id = response.json()["sessionId"]
            print(f"Started session: {self.session_id}")
        except Exception as e:
            print(f"Failed to start session: {e}")
            self.session_id = None

    @task
    def send_chat_message_and_receive_sse(self):
        """
        Sends a chat message and processes the SSE stream, updating global metrics.
        """
        if not self.session_id:
            print(f"No session ID, attempting to start a new one.")
            self.start_chat_session()
            if not self.session_id:
                print(f"Failed to get session ID after retry, skipping task.")
                return

        chat_message_id = str(uuid.uuid4())
        payload = {
            "message": TEST_MESSAGE,
            "sessionId": self.session_id,
            "chatMessageId": chat_message_id
        }

        print(f"Sending message {chat_message_id} for session {self.session_id}")
        try:
            with self.client.post(
                "/api/chat",
                json=payload,
                stream=True,
                name="/api/chat [SSE]",
                catch_response=True,
            ) as response:
                response.raise_for_status()
                client = sseclient.SSEClient(response.raw)
                chunk_count = 0
                start_time = time.time()
                for event in client.events():
                    if event.event == 'message':
                        if event.data == "__END__":
                            break
                        try:
                            data = json.loads(event.data)
                            if "token" in data:
                                chunk_count += 1
                        except json.JSONDecodeError:
                            pass
                end_time = time.time()
                duration = end_time - start_time
                print(f"Finished SSE stream for {chat_message_id}. Chunks: {chunk_count}, Duration: {duration:.2f}s")
                # Update global metrics for this request type
                name = "/api/chat [SSE]"
                metrics = sse_stats.setdefault(name, {"Total SSE Chunks": 0.0, "Processed SSE Streams": 0.0, "Total SSE Stream Time (s)": 0.0})
                metrics["Total SSE Chunks"] += chunk_count
                metrics["Processed SSE Streams"] += 1
                metrics["Total SSE Stream Time (s)"] += duration
                metrics["Avg Chunks/Stream"] = round(metrics["Total SSE Chunks"] / metrics["Processed SSE Streams"], 2)
                metrics["Avg SSE Stream Time (s)"] = round(metrics["Total SSE Stream Time (s)"] / metrics["Processed SSE Streams"], 2)
                if chunk_count == 0 and duration < 0.1:
                    response.failure("No chunks received or stream ended too quickly")
                else:
                    response.success()
        except Exception as e:
            print(f"Error during chat/SSE for {chat_message_id}: {e}")
            # Update metrics for failed stream
            name = "/api/chat [SSE]"
            metrics = sse_stats.setdefault(name, {"Total SSE Chunks": 0.0, "Processed SSE Streams": 0.0, "Total SSE Stream Time (s)": 0.0})
            metrics["Processed SSE Streams"] += 1
            metrics["Avg Chunks/Stream"] = round(metrics["Total SSE Chunks"] / metrics["Processed SSE Streams"], 2)
            metrics["Avg SSE Stream Time (s)"] = round(metrics["Total SSE Stream Time (s)"] / metrics["Processed SSE Streams"], 2)
            if 'response' in locals() and response is not None:
                response.failure(str(e))
