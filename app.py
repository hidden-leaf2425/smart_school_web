from flask import Flask, render_template
import threading
import paho.mqtt.client as mqtt

app = Flask(__name__)

# Cấu hình MQTT
MQTT_BROKER = "broker.hivemq.com"  # Thay bằng MQTT broker của bạn
MQTT_PORT = 1883
MQTT_TOPIC = "home/test"

# Biến lưu trữ dữ liệu nhận được
received_data = {"message": "No data yet"}

# Xử lý khi kết nối thành công đến MQTT broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)

# Xử lý khi nhận được dữ liệu từ MQTT broker
def on_message(client, userdata, msg):
    global received_data
    received_data["message"] = msg.payload.decode()  # Cập nhật dữ liệu nhận được
    print(f"Received message: {msg.topic} -> {received_data['message']}")

# Khởi động MQTT client trong luồng riêng
def start_mqtt():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()

# Route chính để hiển thị dữ liệu trên web
@app.route('/')
def index():
    return render_template("index.html", data=received_data)

if __name__ == "__main__":
    # Khởi động MQTT client trong luồng riêng để không làm gián đoạn Flask
    mqtt_thread = threading.Thread(target=start_mqtt)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    app.run(host='0.0.0.0', port=5000)
