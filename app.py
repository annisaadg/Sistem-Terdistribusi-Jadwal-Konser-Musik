import datetime
from flask import Flask, request, render_template, redirect, url_for
from flask_socketio import SocketIO
from Subscribe import Subscribe
from SMPublisher import SMPublisher
from YGPublisher import YGPublisher

app = Flask(__name__)
socketio = SocketIO(app)  # Initialize Flask-SocketIO

# Initialize MQTT Publishers
sm_publisher = SMPublisher()
yg_publisher = YGPublisher()

# Initialize MQTT Subscriber
subscriber = Subscribe(sm_publisher, yg_publisher)
subscriber.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/publish/<agency>', methods=['GET', 'POST'])
def publish(agency):
    if request.method == 'POST':
        pesan = request.form['message']
        jadwal = request.form['schedule']
        jadwal_dt = datetime.datetime.strptime(jadwal, "%Y/%m/%d - %H:%M")
        
        if agency == 'SMTOWN':
            feedback = sm_publisher.publish(pesan, jadwal_dt)
        elif agency == 'YG':
            feedback = yg_publisher.publish(pesan, jadwal_dt)
        else:
            feedback = "Invalid agency"
        
        return render_template('publish.html', feedback=feedback, agency=agency)
    return render_template('publish.html', feedback='', agency=agency)

@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        action = request.form['action']
        topic = request.form['topic']
        
        if action == 'subscribe':
            feedback = subscriber.subscribe(topic)
        elif action == 'unsubscribe':
            feedback = subscriber.unsubscribe(topic)
        else:
            feedback = "Invalid action"

        return render_template('subscribe.html', feedback=feedback, subs=subscriber.subs, topics=["SMTOWN", "YG Entertainment"], messages=subscriber.messages)
    return render_template('subscribe.html', feedback='', subs=subscriber.subs, topics=["SMTOWN", "YG Entertainment"], messages=subscriber.messages)

@app.route('/shutdown')
def shutdown():
    subscriber.stop()
    return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app, debug=True)