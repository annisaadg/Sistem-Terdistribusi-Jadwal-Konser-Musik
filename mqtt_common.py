from paho.mqtt import client as mqtt_client

# Detail broker dan otentikasi
broker = 'broker.emqx.io'
port = 1883
username = 'konser'
password = 'konser123'

# Fungsi yang dapat digunakan kembali untuk menghubungkan ke broker MQTT
def connect_mqtt(client_id, agensi):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Terhubung dengan MQTT Broker - {client.agensi}!") # Cetak pesan sukses saat terhubung berhasil
        else:
            print(f"Gagal Terhubung, return code {rc}\n") # Cetak pesan gagal saat terhubung gagal

    client = mqtt_client.Client(client_id) # Membuat instance klien MQTT baru
    client.agensi = agensi # Menetapkan nama agensi untuk klien
    client.username_pw_set(username, password) # Menetapkan nama pengguna dan kata sandi untuk klien
    client.on_connect = on_connect # Menetapkan callback on_connect
    client.connect(broker, port) # Menghubungkan ke broker
    return client # Mengembalikan instance klien yang terhubung
