import random
from mqtt_common import connect_mqtt  # Import the reusable function

# Kelas untuk mengirim pesan ke topik "SMTOWN"
class SMPublisher:
    def __init__(self):
        self.topic = "SMTOWN" # Topik untuk mengirim pesan
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}' # Menghasilkan ID klien acak
        self.client = connect_mqtt(self.client_id, "SMTOWN") # Menghubungkan ke broker MQTT dengan ID klien dan nama agensi

    def publish(self, pesan):
        msg = f"{pesan}" # Memformat pesan
        result = self.client.publish(self.topic, msg, retain=True) # Mengirim pesan ke topik dengan flag retain diatur ke true
        status = result[0] # Mendapatkan status dari operasi publish
        if status == 0:
            return f"Mengirim {msg} ke topik {self.topic}" # Mengembalikan pesan sukses
        else:
            return f"Gagal mengirim pesan ke topik {self.topic}" # Mengembalikan pesan gagal

    def start(self):
        self.client.loop_start() # Memulai loop klien MQTT

    def stop(self):
        self.client.loop_stop() # Menghentikan loop klien MQTT
