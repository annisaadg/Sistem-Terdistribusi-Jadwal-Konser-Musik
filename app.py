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
        # Data Informasi Konser
        pesan = request.form['pesan']
        tanggal = request.form['tanggal']
        waktu = request.form['waktu']
        nama_konser = request.form['nama_konser']
        lokasi = request.form['lokasi']
        harga_tiket = request.form['harga_tiket']
        tema_konser = request.form['tema_konser']

        #Data Informasi Artis
        artists = request.form.getlist('artists')

        # Format the artists list as HTML list
        artists_list_html = "<ul>"
        for artist in artists:
            artists_list_html += f"<li>{artist}</li>"
        artists_list_html += "</ul>"

        # Format the ticket price as Rupiah
        harga_tiket_won = f"{int(harga_tiket):,} KRW".replace(",", ".")

        # Create the full message with all details
        full_message = (
            f"\n{pesan}\n"
            f"Date: {tanggal}\n"
            f"Time: {waktu}\n"
            f"Concert Name: {nama_konser}\n"
            f"Location: {lokasi}\n"
            f"Ticket Price: {harga_tiket_won}\n"
            f"Tema: {tema_konser}\n"
            f"Artists:\n{artists_list_html}"
        )

        if agency == 'SMTOWN':
            feedback = sm_publisher.publish(full_message)
        elif agency == 'YG':
            feedback = yg_publisher.publish(full_message)
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
