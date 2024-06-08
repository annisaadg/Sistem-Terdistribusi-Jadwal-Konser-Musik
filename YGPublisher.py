import random
import datetime
from mqtt_common import connect_mqtt  # Import the reusable function

class YGPublisher:
    def __init__(self):
        self.topic = "YG Entertainment"
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.client = connect_mqtt(self.client_id, "YG Entertainment")

    def publish(self, pesan):
        msg = f"{pesan}"
        result = self.client.publish(self.topic, msg, retain=True)
        status = result[0]
        if status == 0:
            return f"Mengirim {msg} ke topik {self.topic}"
        else:
            return f"Gagal mengirim pesan ke topik {self.topic}"

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
