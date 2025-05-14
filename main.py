#Importing libraries
from pathlib import Path
from logzero import logger, logfile
from sense_hat import SenseHat
from orbit import ISS
from gpiozero import MotionSensor
from time import sleep
from datetime import datetime, timedelta
import random
import csv

#Defining a function to create a new CSV file with the appropriate headers
def create_csv_file(data_file):
    """Create a new CSV file and add the header row"""
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Counter", "Date/time", "Latitude", "Longitude", "Temperature", "Humidity", "Pressure", "Motion_Detected")
        writer.writerow(header)

#Defining a function to write the collected data on to the file created
def add_csv_data(data_file, data):
    """Add a row of data to the data_file CSV"""
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

# Define some colours — keep brightness low
g = [255,255,255]
o = [0,0,0]

# Define a simple image
image = [
    g,g,g,g,g,g,g,g,
    o,g,o,o,o,o,g,o,
    o,o,g,o,o,g,o,o,
    o,o,o,g,g,o,o,o,
    o,o,o,g,g,o,o,o,
    o,o,g,g,g,g,o,o,
    o,g,g,g,g,g,g,o,
    g,g,g,g,g,g,g,g,
]

# Define a function to update the LED matrix
def active_status():
    # A list with all possible rotation values
    rotation_values = [0,90,180,270]
    # Pick one at random
    rotation = random.choice(rotation_values)
    # Set the rotation
    sense.set_rotation(rotation)
    # Display the image
    sense.set_pixels(image)
    
#Setting the base folder to store the data file
base_folder = Path(__file__).parent.resolve()

# Set a logfile name
logfile(base_folder/"events.log")

# Set up Sense Hat
sense = SenseHat()

#Assigning the pin number of motion sensor to a variable
pir = MotionSensor(pin=12)

# Initialise the CSV file
data_file = base_folder/"Readings.csv"
create_csv_file(data_file)

# Initialise the photo counter
counter = 1

# Record the start and current time
start_time = datetime.now()
now_time = datetime.now()

# Run a loop for (almost) three hours
while (now_time < start_time + timedelta(minutes=178)):
    try:
        #Getting humidity and temperature in to the respective variables
        humidity = round(sense.humidity, 4)
        temperature = round(sense.temperature, 4)
        pressure = round(sense.pressure, 4)
        
        # Get coordinates of location on Earth below the ISS
        location = ISS.coordinates()
        
        #Checking if there was a motion and then storing the boolean result in to a variable
        Motion = pir.motion_detected
        
        # Save the data to the file
        data = (
            counter,
            datetime.now(),
            location.latitude.degrees,
            location.longitude.degrees,             
            temperature,
            humidity,
            pressure,
            Motion,
        )
        add_csv_data(data_file, data)
        
        # Log event
        logger.info(f"iteration {counter}")
        counter += 1
        
        sleep(4)
        
        # Update the LED matrix
        active_status()
        
        #sleep(4)
        
        # Update the current time
        now_time = datetime.now()
        
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e}')