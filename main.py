import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase (Use your own credentials)
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smartfarmadvisorsystem-default-rtdb.firebaseio.com/'
})

# References to sensor data
humidity_ref = db.reference('sensor/humidity')
temperature_ref = db.reference('sensor/temperature')
pressure_ref = db.reference('sensor/pressure')
soilMoisture_ref = db.reference('sensor/soilMoisture')
light_ref = db.reference('sensor/light')

# Lists to store last 10 values
humidity_list = []
temperature_list = []
pressure_list = []
soilMoisture_list = []
light_list = []

# Function to fetch and update lists
def fetch_and_update():
    global humidity_list, temperature_list, pressure_list, soilMoisture_list, light_list
    
    # Get the latest humidity and temperature values
    humidity_data = humidity_ref.get()
    temperature_data = temperature_ref.get()
    pressure_data = pressure_ref.get()
    soilMoisture_data = soilMoisture_ref.get()
    light_data = light_ref.get()
    
    # Extract sorted values
    if humidity_data:
        sorted_humidity = sorted(humidity_data.items(), key=lambda x: int(x[0]))  # Sort by timestamp
        humidity_values = [value for _, value in sorted_humidity][-10:]  # Get last 10 values
        humidity_list = humidity_values  # Update list
    
    if temperature_data:
        sorted_temperature = sorted(temperature_data.items(), key=lambda x: int(x[0]))  # Sort by timestamp
        temperature_values = [value for _, value in sorted_temperature][-10:]  # Get last 10 values
        temperature_list = temperature_values  # Update list

    if pressure_data:
        sorted_pressure = sorted(pressure_data.items(), key=lambda x: int(x[0]))  # Sort by timestamp
        pressure_values = [value for _, value in sorted_pressure][-10:]  # Get last 10 values
        pressure_list = pressure_values  # Update list
    
    if soilMoisture_data:
        sorted_soilMoisture = sorted(soilMoisture_data.items(), key=lambda x: int(x[0]))  # Sort by timestamp
        soilMoisture_values = [value for _, value in sorted_soilMoisture][-10:]  # Get last 10 values
        soilMoisture_list = soilMoisture_values  # Update list

    if light_data:
        sorted_light = sorted(light_data.items(), key=lambda x: int(x[0]))  # Sort by timestamp
        light_values = [value for _, value in sorted_light][-10:]  # Get last 10 values
        light_list = light_values  # Update list

    print("Humidity List:", humidity_list)
    print("Temperature List:", temperature_list)
    print("Pressure List:", pressure_list)
    print("SoilMoisture List:", soilMoisture_list)
    print("Light List:", light_list)

# Fetch and update data
fetch_and_update()
