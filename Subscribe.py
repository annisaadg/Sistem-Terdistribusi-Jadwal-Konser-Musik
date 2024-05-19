# Subscribe.py
import random
from mqtt_common import connect_mqtt  # Import the reusable function

class Subscribe:
    def __init__(self, sm_publisher, yg_publisher):
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.client = connect_mqtt(self.client_id, "Subscriber")
        self.subs = []
        self.messages = []  # List to store received messages
        self.sm_publisher = sm_publisher
        self.yg_publisher = yg_publisher
        self.sm_publisher.start()
        self.yg_publisher.start()

    def on_message(self, client, userdata, msg):
        message = f"Received `{msg.payload.decode()}` from `{msg.topic}` topic"
        print(message)
        self.messages.append(message)  # Store received message

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
