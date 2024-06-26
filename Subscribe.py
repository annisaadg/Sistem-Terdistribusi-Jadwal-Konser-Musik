import random
import datetime
from paho.mqtt import client as mqtt_client
from mqtt_common import connect_mqtt  # Import the reusable function

# Kelas untuk berlangganan topik dan menangani pesan yang diterima
class Subscribe:
    def __init__(self, messages):
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}' # Menghasilkan ID klien acak
        self.client = connect_mqtt(self.client_id, "Subscriber") # Menghubungkan ke broker MQTT dengan ID klien dan nama subscriber
        self.subs = [] # Daftar untuk melacak topik yang dilanggan
        self.messages = messages # Referensi ke daftar pesan global

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
            self.subs.append(topic) # Menambahkan topik ke daftar langganan jika belum dilanggan
            self.client.subscribe(topic, qos=0) # Berlangganan ke topik
            return f"Subscribed to {topic}" # Mengembalikan pesan sukses
        else:
            return f"Already subscribed to {topic}" # Mengembalikan pesan sudah berlangganan

    def unsubscribe(self, topic):
        if topic in self.subs:
            self.subs.remove(topic) # Menghapus topik dari daftar langganan jika dilanggan
            self.client.unsubscribe(topic) # Membatalkan langganan dari topik
            return f"Unsubscribed from {topic}" # Mengembalikan pesan sukses
        else:
            return f"Not subscribed to {topic}" # Mengembalikan pesan belum berlangganan

    def start(self):
        self.client.loop_start() # Memulai loop klien MQTT
        self.client.on_message = self.on_message # Menetapkan callback on_message

    def stop(self):
        self.client.loop_stop() # Menghentikan loop klien MQTT

