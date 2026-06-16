import serial
import time
import json
import paho.mqtt.client as mqtt

# ==================== CONFIGURATION ====================
SERIAL_PORT = 'COM3'  # <-- Double check your actual Arduino port!
BAUD_RATE = 9600
MQTT_BROKER = "157.173.101.159"  # Your VPS IP
MQTT_PORT = 1883

# Matching the target channels on your HTML layout
TOPIC_DATA = "sensors/dht"
TOPIC_LED_CMD = "control/led"
TOPIC_LED_STATE = "control/led/status"

USER_NAME = "Ishara Gold"
# =======================================================

mqtt_client = mqtt.Client()

# Callback: Receives interaction updates from the browser dashboard
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    if message.topic == TOPIC_LED_CMD:
        print(f"[*] Actuator command received from Web Panel: {payload}")
        # Bounce message state back out to finalize button UI sync
        mqtt_client.publish(TOPIC_LED_STATE, payload)

mqtt_client.on_message = on_message

try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.subscribe(TOPIC_LED_CMD)
    mqtt_client.loop_start()
    print(f"[*] Connected to VPS Broker at {MQTT_BROKER}")
except Exception as e:
    print(f"[!] MQTT Connection Failed: {e}")
    exit(1)

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) 
    print(f"[*] Reading USB Data from Arduino on {SERIAL_PORT}")
except Exception as e:
    print(f"[!] USB Connection Failed: {e}. Ensure Arduino IDE Monitor is closed.")
    exit(1)

print(f"\n--- Ingestion Node Online | Operator: {USER_NAME} ---")

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                if line == "Error":
                    print(f"[{time.strftime('%H:%M:%S')}] Sensor error detected on hardware node.")
                    continue
                try:
                    temp_value = float(line)
                    timestamp = time.strftime("%H:%M:%S")
                    
                    print(f"[{timestamp}] User: {USER_NAME} | Ingested Temp: {temp_value} °C")
                    
                    # Packaging dataset frame to comply with frontend Chart.js parsing mechanics
                    payload_dict = {
                        "temperature": temp_value,
                        "humidity": 0.0  # Safe static default value
                    }
                    json_payload = json.dumps(payload_dict)
                    
                    # Push downstream payload out over broker pipe
                    mqtt_client.publish(TOPIC_DATA, json_payload)
                    
                except ValueError:
                    pass
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nSafely wrapping up operations...")
finally:
    ser.close()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()