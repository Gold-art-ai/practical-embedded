import serial
import time
import paho.mqtt.client as mqtt

# ==================== CONFIGURATION ====================
SERIAL_PORT = 'COM3'  # <-- Change to your actual Arduino port!
BAUD_RATE = 9600
MQTT_BROKER = "your_vps_ip_here" # <-- Input your Cloud VPS IP
MQTT_PORT = 1883
MQTT_TOPIC = "home/temperature"
# =======================================================

mqtt_client = mqtt.Client()

try:
    # Optional: Uncomment if your VPS MQTT broker requires a password
    # mqtt_client.username_pw_set("username", "password")
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print(f"[*] Connected to VPS MQTT Broker at {MQTT_BROKER}")
    mqtt_client.loop_start()
except Exception as e:
    print(f"[!] MQTT Connection Failed: {e}")
    exit(1)

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) # Arduino boot stabilization delay
    print(f"[*] Reading USB Data from Arduino on {SERIAL_PORT}")
except Exception as e:
    print(f"[!] USB Connection Failed: {e}. Is the Arduino IDE serial monitor still open?")
    exit(1)

print("\n--- Live Data Stream ---")

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                if line == "Error":
                    print("[ALERT] Arduino is reporting a sensor read fault!")
                    continue
                try:
                    temp_value = float(line)
                    timestamp = time.strftime("%H:%M:%S")
                    
                    # Task: Real-time display on PC monitor
                    print(f"[{timestamp}] Temp: {temp_value} °C")
                    
                    # Task: Publish directly to the cloud MQTT broker
                    mqtt_client.publish(MQTT_TOPIC, str(temp_value))
                except ValueError:
                    pass
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nShutting down stream safely...")
finally:
    ser.close()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("[*] Successfully closed.")