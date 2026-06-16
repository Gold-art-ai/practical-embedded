#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

#define DHTPIN 2          // Sensor Data pin connected to Digital Pin 2
#define DHTTYPE DHT11     // Standard Blue Grid Sensor
const int sensorPowerPin = 3; // Software-controlled 5V power pin for the sensor

DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2); // Standard I2C address for 16x2 screens

String nameStr = "Ishara Gold"; // Your name
int scrollPos = 0;
unsigned long lastUpdate = 0;
const long interval = 2000;    // DHT11 refreshes best every 2 seconds

void setup() {
  // Turn Digital Pin 3 into a 5V power source instantly
  pinMode(sensorPowerPin, OUTPUT);
  digitalWrite(sensorPowerPin, HIGH);

  Serial.begin(9600); // Start USB communication with your PC
  lcd.init();
  lcd.backlight();
  dht.begin();        
  
  if (nameStr.length() > 16) {
    nameStr += "   "; // Smooth padding if the name is extra long
  }
}

void loop() {
  unsigned long currentMillis = millis();

  // Task: Read temperature and output to USB every 2 seconds
  if (currentMillis - lastUpdate >= interval) {
    lastUpdate = currentMillis;

    float temperatureC = dht.readTemperature();

    if (isnan(temperatureC)) {
      Serial.println("Error"); 
      lcd.setCursor(0, 1);
      lcd.print("Sensor Error    ");
    } else {
      // Send raw value via USB to the PC program
      Serial.println(temperatureC, 2); 

      // Display real-time data on LCD row 2
      lcd.setCursor(0, 1);
      lcd.print("Temp: ");
      lcd.print(temperatureC, 1);
      lcd.print((char)223); // Degree symbol (°)
      lcd.print("C   ");   
    }
  }

  // Task: Scroll name smoothly on row 1
  static unsigned long lastScroll = 0;
  if (millis() - lastScroll >= 400) { 
    lastScroll = millis();
    
    lcd.setCursor(0, 0);
    if (nameStr.length() <= 16) {
      lcd.print(nameStr); // Static display if it fits perfectly
    } else {
      String displayStr = nameStr.substring(scrollPos) + nameStr.substring(0, scrollPos);
      lcd.print(displayStr.substring(0, 16));
      scrollPos++;
      if (scrollPos >= nameStr.length()) {
        scrollPos = 0;
      }
    }
  }
}