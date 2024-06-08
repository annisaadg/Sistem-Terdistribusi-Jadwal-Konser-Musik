import datetime
from flask import Flask, request, render_template, redirect, url_for
from SMPublisher import SMPublisher
from YGPublisher import YGPublisher
from Subscribe import Subscribe

app = Flask(__name__)
messages = []  # Daftar pesan global untuk menyimpan pesan MQTT yang diterima

# Inisialisasi Klien MQTT
sm_publisher = SMPublisher()
yg_publisher = YGPublisher()
subscriber = Subscribe(messages)

@app.route('/')
def index():
    return render_template('index.html') # Menampilkan halaman indeks

@app.route('/publish/<agency>', methods=['GET', 'POST'])
def publish(agency):
    if request.method == 'POST':
        pesan = request.form['message']
        jadwal = request.form['schedule']
        jadwal_dt = datetime.datetime.strptime(jadwal, "%Y/%m/%d - %H:%M") # Mengonversi string jadwal menjadi objek datetime
        
        if agency == 'SMTOWN':
            feedback = sm_publisher.publish(pesan, jadwal_dt) # Mengirim pesan menggunakan SMPublisher
        elif agency == 'YG':
            feedback = yg_publisher.publish(pesan, jadwal_dt) # Mengirim pesan menggunakan YGPublisher
        else:
            feedback = "Invalid agency" # Menangani agensi tidak valid
        
        return render_template('publish.html', feedback=feedback, agency=agency) # Menampilkan halaman publish dengan feedback
    return render_template('publish.html', feedback='', agency=agency) # Menampilkan halaman publish

@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        action = request.form['action']
        topic = request.form['topic']
        
        if action == 'subscribe':
            feedback = subscriber.subscribe(topic) # Berlangganan ke topik
        elif action == 'unsubscribe':
            feedback = subscriber.unsubscribe(topic) # Membatalkan langganan dari topik
        else:
            feedback = "Invalid action" # Menangani tindakan tidak valid

        return render_template('subscribe.html', feedback=feedback, subs=subscriber.subs, topics=["SMTOWN", "YG Entertainment"], messages=messages) # Menampilkan halaman subscribe dengan feedback
    return render_template('subscribe.html', feedback='', subs=subscriber.subs, topics=["SMTOWN", "YG Entertainment"], messages=messages) # Menampilkan halaman subscribe

@app.route('/setup')
def setup():
    sm_publisher.start() # Memulai loop klien SMPublisher
    yg_publisher.start() # Memulai loop klien YGPublisher
    subscriber.start() # Memulai loop klien Subscribe
    return redirect(url_for('index'))# Mengarahkan ke halaman indeks

@app.route('/shutdown')
def shutdown():
    sm_publisher.stop() # Menghentikan loop klien SMPublisher
    yg_publisher.stop() # Menghentikan loop klien YGPublisher
    subscriber.stop() # Menghentikan loop klien Subscribe
    return redirect(url_for('index')) # Mengarahkan ke halaman indeks

if __name__ == '__main__':
    app.run(debug=True)
