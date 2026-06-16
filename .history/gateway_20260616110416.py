import serial
import time
import paho.mqtt.client as mqtt

# ==================== CONFIGURATION ====================
SERIAL_PORT = 'COM3'  # <-- Double check your actual Arduino port!
BAUD_RATE = 9600
MQTT_BROKER = "your_vps_ip_here" # <-- Input your Cloud VPS IP
MQTT_PORT = 1883
MQTT_TOPIC = "home/temperature"

# Your name to display on the PC monitor
USER_NAME = "Ishara Gold"
# =======================================================

mqtt_client = mqtt.Client()

try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print(f"[*] Connected to VPS MQTT Broker at {MQTT_BROKER}")
    mqtt_client.loop_start()
except Exception as e:
    print(f"[!] MQTT Connection Failed: {e}")
    exit(1)

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) 
    print(f"[*] Reading USB Data from Arduino on {SERIAL_PORT}")
except Exception as e:
    print(f"[!] USB Connection Failed: {e}")
    exit(1)

print(f"\n--- Live Data Stream for Monitor: {USER_NAME} ---")
print("-" * 50)

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                if line == "Error":
                    print(f"[{time.strftime('%H:%M:%S')}] [{USER_NAME}] ALERT: Sensor fault!")
                    continue
                try:
                    temp_value = float(line)
                    timestamp = time.strftime("%H:%M:%S")
                    
                    # TASK FIXED: Real-time display on PC monitor featuring your name!
                    print(f"[{timestamp}] User: {USER_NAME} | Live Temp: {temp_value} °C")
                    
                    # Broadcast to cloud VPS
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