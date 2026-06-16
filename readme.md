# Simple Temp Monitor 🌡️

A quick project that reads temperature using an Arduino and sends it to the cloud.

## 📐 System Architecture
This is how the data moves through the system from the room to the cloud:

[Room Temperature]
       │
       ▼ (Reads data)
+-------------------+ 
|   DHT11 Sensor    | 
+-------------------+ 
       │ 
       ▼ (Hardware Wire to Pin 2)
+-------------------+ 
|    Arduino Uno    | <-- Shows "Ishara Gold" & Temp on LCD
+-------------------+ 
       │ 
       ▼ (USB Cable Link)
+-------------------+ 
|    PC Gateway     | <-- Prints live data to your terminal
|  (Python Script)  | 
+-------------------+ 
       │ 
       ▼ (MQTT Protocol over Internet)
+-------------------+ 
|     Cloud VPS     | <-- Receives the data (Topic: home/temperature)
|   (MQTT Broker)   | 
+-------------------+

## 🚀 How It Works
1. **The Sensor (DHT11):** Connected to Digital Pin 2 for data. Pin 3 is hardcoded to give it 5V power so you don't need a breadboard!
2. **The Screen (I2C LCD):** Wired to A4 (SDA) and A5 (SCL). Row 1 scrolls the name "Ishara Gold", Row 2 shows the temperature.
3. **The PC (Python Script):** Grabs the numbers from the USB port, prints them live on your screen, and pushes them to your VPS Cloud Broker.

## 🔌 Quick Wiring Guide
* **DHT11 Sensor:** `+` to Pin 3 | `Out` to Pin 2 | `-` to GND
* **I2C LCD Screen:** `VCC` to 5V | `GND` to GND | `SDA` to A4 | `SCL` to A5

## 🎛️ Network Info
* **Baud Rate:** 9600 (USB Speed)
* **MQTT Port:** 1883
* **MQTT Topic:** `home/temperature`"# practical-embedded" 
