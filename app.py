import random
import datetime
from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit
from paho.mqtt import client as mqtt_client

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

broker = 'broker.emqx.io'
port = 1883
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'konser'
password = 'konser123'
subs = []
mqtt_client_instance = None

def connect_mqtt(client):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}\n")

    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)

def on_message(client, userdata, msg):
    message = f"Received `{msg.payload.decode()}` from `{msg.topic}` topic"
    print(message)
    socketio.emit('mqtt_message', {'topic': msg.topic, 'message': msg.payload.decode()})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/publisher')
def publisher():
    return render_template('publisher.html')

@app.route('/subscriber')
def subscriber():
    return render_template('subscriber.html')

@app.route('/publish', methods=['POST'])
def publish_message():
    data = request.get_json()
    topic = data.get('topic')
    message = data.get('message')
    schedule = data.get('schedule')
    msg = f"{message} jadwal:{schedule}"
    result = mqtt_client_instance.publish(topic, msg, retain=True)
    status = result[0]
    if status == 0:
        return jsonify({"status": "success", "message": f"Sent `{msg}` to topic `{topic}`"})
    else:
        return jsonify({"status": "error", "message": "Failed to send message"})

@app.route('/subscribe', methods=['POST'])
def subscribe_topic():
    data = request.get_json()
    topic = data.get('topic')
    if topic in subs:
        subs.remove(topic)
        mqtt_client_instance.unsubscribe(topic)
    else:
        subs.append(topic)
        mqtt_client_instance.subscribe(topic)
    return jsonify({"status": "success", "subs": subs})

@app.route('/init', methods=['GET'])
def init_client():
    global mqtt_client_instance
    mqtt_client_instance = mqtt_client.Client(client_id)
    mqtt_client_instance.on_message = on_message
    connect_mqtt(mqtt_client_instance)
    mqtt_client_instance.loop_start()
    return jsonify({"status": "initialized"})

if __name__ == '__main__':
    socketio.run(app, debug=True)
