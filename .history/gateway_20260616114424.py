import streamlit as str
import serial
import time
import paho.mqtt.client as mqtt

# ==================== CONFIGURATION ====================
SERIAL_PORT = 'COM3'  # <-- Change to your actual Arduino port!
BAUD_RATE = 9600
MQTT_BROKER = "your_vps_ip_here" # <-- Input your Cloud VPS IP
MQTT_PORT = 1883
MQTT_TOPIC = "home/temperature"
USER_NAME = "Ishara Gold"
# =======================================================

# Web Dashboard UI Setup
str.set_page_config(page_title="IoT Dashboard", layout="centered")
str.title(f"🌡️ Real-Time Telemetry Dashboard")
str.subheader(f"Monitor Operator: {USER_NAME}")

# Create UI placeholders that update live
metric_box = str.empty()
status_box = str.empty()

# Setup MQTT
mqtt_client = mqtt.Client()
try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
    status_box.success("✅ Connected to VPS MQTT Broker")
except Exception as e:
    status_box.error(f"❌ MQTT Connection Failed: {e}")

# Setup Serial Connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) # Buffer for Arduino reboot
except Exception as e:
    str.error(f"❌ USB Connection Failed on {SERIAL_PORT}. Check port or close Arduino IDE Serial Monitor.")
    st.stop()

# Real-Time Data Reading and UI Update Loop
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        if line:
            if line == "Error":
                metric_box.metric(label="Current Temperature", value="SENSOR ERROR", delta="Check Wires")
                continue
            try:
                temp_value = float(line)
                timestamp = time.strftime("%H:%M:%S")
                
                # 1. Update the Web Dashboard screen in real-time
                metric_box.metric(label=f"Live Temp (Last updated: {timestamp})", value=f"{temp_value} °C")
                
                # 2. Print to Console (Real-time terminal display)
                print(f"[{timestamp}] User: {USER_NAME} | Temp: {temp_value} °C")
                
                # 3. Publish to Cloud VPS
                mqtt_client.publish(MQTT_TOPIC, str(temp_value))
            except ValueError:
                pass
    time.sleep(0.1)