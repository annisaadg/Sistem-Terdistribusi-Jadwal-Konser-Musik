from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
username = 'konser'
password = 'konser123'

def connect_mqtt(client_id, agensi):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Terhubung dengan MQTT Broker - {client.agensi}!")
        else:
            print(f"Gagal Terhubung, return code {rc}\n")

    client = mqtt_client.Client(client_id)
    client.agensi = agensi
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
