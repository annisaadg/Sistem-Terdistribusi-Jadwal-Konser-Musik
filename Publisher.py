import random
import time
import datetime

from paho.mqtt import client as mqtt_client

#CONFIG
broker = 'broker.emqx.io'
port = 1883
topic = ""
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'grup6'
password = 'public'

def connect_mqtt():
	#Connect publisher ke broker
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


def publish(client):
    command = 1
    while (command != 0):
    	#MENU PUBLISH
	    print("perintah : \n 0 untuk keluar \n 1 untuk melakukan publish")
	    command = input()
	    if command == str(0):
	        exit()
	    if command == str(1):
          

	  #INPUT PESAN
	        pesan = input("pesan :")
	        jadwal = datetime.datetime.strptime(
	            input('Jadwal acara `YYYY/mm/dd - HH:MM`  format: '), "%Y/%m/%d - %H:%M")
	        msg = f"{pesan} jadwal:{jadwal}"
	        
	        #PUBLISH ke BROKER
	        result = client.publish(topic, msg)
	        status = result[0]
	        if status == 0:
	            print(f"Mengirim `{msg}` ke topik `{topic}`")
	        else:
	            print(f"Gagal mengirim pesan ke topic {topic}")
	        print ()

	        client.loop_start()
	        client.loop_stop()

def agensi():
	#Fungsi untuk pemilihan agensi
	global topic
	print("==========Menu==========")
	SM = "SMTOWN"
	YG = "YG Entertaiment"
	print(f"AGENSI : \n 1 {SM} \n 2 {YG}")
	print("========================")
	command = input()
	if command == str(1):
		topic = SM
	elif command == str(2):
		topic = YG
	print()
	

def run():
	global topic 
	agensi()
	print (topic)
	client = connect_mqtt()
	client.loop_start()
	publish(client)

if __name__ == '__main__':
    run()

time.sleep(300)    
