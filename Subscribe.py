import random
import time
from paho.mqtt import client as mqtt_client

#CONFIG
broker = 'broker.emqx.io'
port = 1883
topic = "SMTOWN", "YG Entertaiment"
client_id = ""
username = 'grup6'
password = 'public'
subs = []

def connect_mqtt(client: mqtt_client):
    #Connect subscriber ke broker
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Terhubung MQTT Broker!\n")
        else:
            print("Gagal Terhubung,  %d\n", rc)

    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)

def on_message(client, userdata, msg):
    #Mendapatkan PESAN dari PUBLISHER
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

def subscribe_menu(client):
    #Memilih untuk subscribe/unsubscribe topik
    SM = "SMTOWN"
    YG = "YG Entertaiment"
    print(f"sekarang sedang subscribe {subs}")
    print(f"subscribe/unsubscribe : \n 1 {SM} \n 2 {YG}")
    command = input()
    if command == str(1):
        #Bagian untuk proses subscribe dan unsubscribe untuk SMTOWN
        if SM in subs: 
            subs.pop(subs.index(SM))
            client.unsubscribe(SM)
        else:
            subs.append(SM)
            client.subscribe(SM)
    elif command == str(2):
        #Bagian untuk proses subscribe dan un subsribe untuk YG Entertainment
        if YG in subs:
            subs.pop(subs.index(YG))
            client.unsubscribe(YG)
        else:
            subs.append(YG)
            client.subscribe(YG)
    print(f"selamat bergabung di {subs}")
    print()
    print()

def run():
    global client_id
    client_id = input("Nama : ")

    #Membuat Client
    client = mqtt_client.Client(client_id)

    #Connect client ke broker
    connect_mqtt(client)

    #Start loop client
    client.loop_start()
    time.sleep(1)

    subscribe_menu(client)

    while True:
        client.on_message = on_message    
        inputs = input()
        if (inputs == "menu"):
            subscribe_menu(client)
        time.sleep(1)

    client.loop_stop()

if __name__ == '__main__':
    run()

