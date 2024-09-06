from flask import Flask, render_template, request, jsonify
from env.encode_decode import encode_pesan, decode_pesan
from datetime import datetime
import paho.mqtt.client as mqtt
import requests
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Store temperature data
temperature_data = []

FIREBASE_URL = "https://capstone-63601-default-rtdb.asia-southeast1.firebasedatabase.app/Temp.json"

def read_temperature_from_firebase():
    try:
        response = requests.get(FIREBASE_URL)
        response.raise_for_status()
        data = response.json()
        print(f"Data received from Firebase: {data}")  # Log the received data

        if isinstance(data, dict):
            # Assuming the data is a dictionary of records
            latest_entry = list(data.values())[-1]
            temperature = latest_entry.get('temperature')  # Adjust the key if necessary
            if temperature:
                print(f"Temperature read from Firebase: {temperature}")
                return temperature
            else:
                print("Temperature key not found in the latest entry.")
        elif isinstance(data, list) and data:
            latest_data = data[-1]
            temperature = latest_data.get('temperature')  # Adjust the key if necessary
            if temperature:
                print(f"Temperature read from Firebase: {temperature}")
                return temperature
        print("No valid temperature data received from Firebase.")
        return None
    except requests.RequestException as e:
        print(f"Error reading temperature from Firebase: {e}")
        return None

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT broker.")
    else:
        print(f"Failed to connect to MQTT broker. Code: {rc}")

def terima_pesan_terenkripsi(client, userdata, msg):
    now = datetime.now()
    timestamp = now.strftime("%m/%d/%Y, %H:%M:%S")

    print("Message received from MQTT topic 'pesan'. Decoding...")
    asli, sembunyi, pesan_hasil = decode_pesan(msg.payload.decode())
    asli_pake_spasi = asli.replace("|", " ")

    # Print received message for debugging
    print(f"Message received at {timestamp}:")
    print(f"  Original message: {sembunyi}")
    print(f"  Tersembunyi message: {asli_pake_spasi}")

    # Emit message to WebSocket clients
    socketio.emit('new_message', {'timestamp': timestamp, 'sembunyi': sembunyi, 'asli': asli_pake_spasi})
    print(f"Message emitted to WebSocket clients.")

    # Store message data in a file or database for persistence
    with open("received_messages.txt", "a") as f:
        f.write(f"{timestamp}: {sembunyi}\n")
        f.write(f"{timestamp}: {asli_pake_spasi}\n")

client = mqtt.Client(client_id="", userdata=None, protocol=mqtt.MQTTv5)
client.on_connect = on_connect
# Connect to the local Mosquitto broker without encryption
client.connect("localhost", 1883)

client.message_callback_add("pesan", terima_pesan_terenkripsi)
client.subscribe("pesan", qos=1)
client.loop_start()

@app.route('/')
def index():
    return render_template('sender.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    suhu = read_temperature_from_firebase()
    if suhu is None:
        return "Gagal membaca suhu dari Firebase."

    pesan_tersembunyi = request.form['pesan_tersembunyi']

    pesan_encoded = encode_pesan(str(suhu), pesan_tersembunyi)
    client.publish("pesan", pesan_encoded)

    notifikasi = f"Pesan terenkripsi berhasil dikirim"
    print(notifikasi) 
    return notifikasi

@app.route('/receiver')
def receiver():
    return render_template('receiver.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/temp')
def temp():
    return render_template('temp.html')

@app.route('/send_temperature')
def send_temperature():
    temperature = read_temperature_from_firebase()
    if temperature:
        client.publish("temperature", temperature)
        temperature_data.append({"timestamp": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "temperature": temperature})
        return f"Temperature sent: {temperature}"
    else:
        return "Failed to read temperature from Firebase."

@app.route('/temperature_data')
def get_temperature_data():
    return jsonify(temperature_data)

@app.route('/view_temperature')
def view_temperature():
    return render_template('view_temperature.html', data=temperature_data)

if __name__ == '__main__':
    socketio.run(app, debug=True)
