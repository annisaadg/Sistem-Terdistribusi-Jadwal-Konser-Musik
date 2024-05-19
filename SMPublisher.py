import random
from mqtt_common import connect_mqtt
from app import socketio  # Import Flask-SocketIO

class SMPublisher:
    def __init__(self):
        self.topic = "SMTOWN"
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.client = connect_mqtt(self.client_id, "SMTOWN")

    def publish(self, pesan, jadwal):
        msg = f"{pesan} jadwal:{jadwal}"
        result = self.client.publish(self.topic, msg, retain=True)
        status = result[0]
        if status == 0:
            # Emit message via WebSocket
            socketio.emit('mqtt_message', msg, namespace='/mqtt')
            return f"Mengirim {msg} ke topik {self.topic}"
        else:
            return f"Gagal mengirim pesan ke topik {self.topic}"

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()