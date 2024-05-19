import random
from app import socketio
from mqtt_common import connect_mqtt  # Import the reusable function

class YGPublisher:
    def __init__(self):
        self.topic = "YG Entertainment"
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.client = connect_mqtt(self.client_id, "YG Entertainment")

    def publish(self, pesan, jadwal):
        msg = f"{pesan} jadwal:{jadwal}"
        result = self.client.publish(self.topic, msg, retain=True)
        status = result[0]
        if status == 0:
            message = f"Mengirim {msg} ke topik {self.topic}"
        else:
            message = f"Gagal mengirim pesan ke topik {self.topic}"
        socketio.emit('message_sent', {'message': message})
        return message

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
