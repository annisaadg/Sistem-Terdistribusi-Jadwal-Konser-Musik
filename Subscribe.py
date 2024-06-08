import random
import datetime
from paho.mqtt import client as mqtt_client
from mqtt_common import connect_mqtt  # Import the reusable function

class Subscribe:
    def __init__(self, messages):
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.client = connect_mqtt(self.client_id, "Subscriber")
        self.subs = []
        self.messages = messages
    
    def on_message(self, client, userdata, msg):
        # Format the received message for better readability
        payload = msg.payload.decode()
        # Replace newline characters with <br> for HTML formatting
        payload_formatted = payload.replace('\n', '<br>')
        formatted_message = (
            f"<strong>Topic:</strong> {msg.topic}<br>"
            f"{payload_formatted}<br><br>"
            f"<strong>Received at:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print(f"Received `{payload}` from `{msg.topic}` topic")
        self.messages.append(formatted_message)

    def subscribe(self, topic):
        if topic not in self.subs:
            self.subs.append(topic)
            self.client.subscribe(topic, qos=0)
            return f"Subscribed to {topic}"
        else:
            return f"Already subscribed to {topic}"

    def unsubscribe(self, topic):
        if topic in self.subs:
            self.subs.remove(topic)
            self.client.unsubscribe(topic)
            return f"Unsubscribed from {topic}"
        else:
            return f"Not subscribed to {topic}"

    def start(self):
        self.client.loop_start()
        self.client.on_message = self.on_message

    def stop(self):
        self.client.loop_stop()
