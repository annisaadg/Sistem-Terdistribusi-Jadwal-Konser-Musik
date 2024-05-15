import random
import time
import datetime

from paho.mqtt import client as mqtt_client

#CONFIG
broker = 'broker.emqx.io'
port = 1883
topic = "SMTOWN"  # Setel topik sesuai dengan agensi
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'konser'
password = 'konser123'

# Fungsi untuk menghubungkan ke broker MQTT
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Terhubung dengan MQTT Broker!")
        else:
            print("Gagal Terhubung, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# Fungsi untuk melakukan publish pesan
def publish(client):
    command = 1
    while (command != 0):
        print("perintah : \n 0 untuk keluar \n 1 untuk melakukan publish")
        command = input()
        if command == str(0):
            exit()
        if command == str(1):
            pesan = input("pesan :")
            jadwal = datetime.datetime.strptime(
                input('Jadwal acara YYYY/mm/dd - HH:MM  format: '), "%Y/%m/%d - %H:%M")
            msg = f"{pesan} jadwal:{jadwal}"
            
            # PUBLISH ke BROKER
            result = client.publish(topic, msg)
            status = result[0]
            if status == 0:
                print(f"Mengirim {msg} ke topik {topic}")
            else:
                print(f"Gagal mengirim pesan ke topic {topic}")
            print()

            client.loop_start()
            client.loop_stop()

# Fungsi untuk menjalankan program
def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()

time.sleep(300)