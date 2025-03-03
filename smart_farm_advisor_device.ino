#include <Wire.h>
#include <DHT.h>
#include <Adafruit_BMP280.h>
#include <ESP8266WiFi.h>
#include <FirebaseESP8266.h>

// WiFi credentials
const char* ssid = "SGKR";  
const char* password = "4321043210";  

// Firebase credentials
#define FIREBASE_HOST "smartfarmadvisorsystem-default-rtdb.firebaseio.com/"
#define FIREBASE_AUTH "NpWI0fkYlcJhw5VEZMghL0Pad2tprhH4kUXiRBtFq"

// Sensor Pins
#define DHTPIN D6
#define DHTTYPE DHT11
#define SOIL_MOISTURE_PIN A0
#define LIGHT_SENSOR_PIN D3  // LDR connected to D3

// Sensor Objects
DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP280 bmp;
FirebaseData firebaseData;
FirebaseAuth auth;
FirebaseConfig config;

// Connect to WiFi
void connectToWiFi() {
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(1000);
    }
    Serial.println("\nConnected to WiFi!");
}

// Connect to Firebase
void connectToFirebase() {
    config.host = FIREBASE_HOST;
    config.signer.tokens.legacy_token = FIREBASE_AUTH;
    Firebase.begin(&config, &auth);
    Firebase.reconnectWiFi(true);
    Serial.println("Connected to Firebase!");
}

// Send data with timestamp to Firebase
void sendData(String path, float value) {
    String timeStamp = String(millis());  // Generate unique key using system time
    String newPath = path + "/" + timeStamp;  // Append timestamp to the path

    if (Firebase.setFloat(firebaseData, newPath, value)) {  
        Serial.print("Sent ");
        Serial.print(value);
        Serial.print(" to ");
        Serial.println(newPath);
    } else {
        Serial.print("Failed to send data: ");
        Serial.println(firebaseData.errorReason());
    }
}

void setup() {
    Serial.begin(9600);
    connectToWiFi();
    connectToFirebase();
    
    dht.begin();
    if (!bmp.begin(0x76)) {
        Serial.println("Could not find BMP280 sensor!");
        while (1);
    }
}

void loop() {
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    float pressure = bmp.readPressure() / 100.0F;
    int soilMoisture = analogRead(SOIL_MOISTURE_PIN);
    int lightValue = digitalRead(LIGHT_SENSOR_PIN);

    // Convert soil moisture reading to percentage
    soilMoisture = map(soilMoisture, 1023, 300, 0, 100);
    soilMoisture = constrain(soilMoisture, 0, 100);

    Serial.println("Sensor Readings:");
    Serial.print("Temperature: "); Serial.println(temperature);
    Serial.print("Humidity: "); Serial.println(humidity);
    Serial.print("Pressure: "); Serial.println(pressure);
    Serial.print("Soil Moisture: "); Serial.println(soilMoisture);
    Serial.print("Light Value: "); Serial.println(lightValue);
    Serial.println("----------------------");

    // Send Data with Unique Timestamp Keys
    sendData("/sensor/temperature", temperature);
    sendData("/sensor/humidity", humidity);
    sendData("/sensor/pressure", pressure);
    sendData("/sensor/soilMoisture", soilMoisture);
    sendData("/sensor/light", lightValue);
    
    delay(3000); // Send data every 3 seconds
}
