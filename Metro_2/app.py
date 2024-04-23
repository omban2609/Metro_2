import RPi.GPIO as GPIO
import time
import Adafruit_DHT
from flask import Flask, render_template, jsonify
import threading

app = Flask(__name__)

# Ultrasonic sensor setup
TRIG = 23
ECHO = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Temperature sensor setup (DHT11)
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # GPIO pin connected to the DHT11 sensor

# Relay GPIO pins for controlling motors
RELAY_PIN_MOTOR1 = 17  # GPIO pin for motor 1
RELAY_PIN_MOTOR2 = 27  # GPIO pin for motor 2
RELAY_PIN_MOTOR3 = 22  # GPIO pin for motor 3
RELAY_PIN_MOTOR4 = 10  # GPIO pin for motor 4

# Global variables
people_count = 0
temperature = 0
humidity = 0
current_station = 1  # Initialize current station to 1
forward_direction = True  # True for forward, False for backward

# Function to measure distance using ultrasonic sensor
def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2
    return distance

# Function to count people entering the metro
def count_people():
    global people_count
    while True:
        distance = measure_distance()
        if distance < 100:  # Adjust this value according to your setup
            people_count += 1
            print("Person entered. Total people:", people_count)
        time.sleep(1)

# Function to read temperature and humidity from DHT sensor
def read_sensor_data():
    global temperature, humidity
    while True:
        humidity, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temp is not None:
            temperature = temp
            print("Temperature inside metro:", temperature)
            print("Humidity inside metro:", humidity)
        time.sleep(5)  # Adjust this value according to your requirements

# Function to control motor 1
def control_motor1(direction):
    if direction == 'forward':
        GPIO.output(RELAY_PIN_MOTOR1, GPIO.HIGH)  # Start motor 1 forward
    elif direction == 'backward':
        GPIO.output(RELAY_PIN_MOTOR1, GPIO.LOW)  # Start motor 1 backward

# Function to control motor 2
def control_motor2(direction):
    if direction == 'forward':
        GPIO.output(RELAY_PIN_MOTOR2, GPIO.HIGH)  # Start motor 2 forward
    elif direction == 'backward':
        GPIO.output(RELAY_PIN_MOTOR2, GPIO.LOW)  # Start motor 2 backward

# Function to control motor 3
def control_motor3(direction):
    if direction == 'forward':
        GPIO.output(RELAY_PIN_MOTOR3, GPIO.HIGH)  # Start motor 3 forward
    elif direction == 'backward':
        GPIO.output(RELAY_PIN_MOTOR3, GPIO.LOW)  # Start motor 3 backward

# Function to control motor 4
def control_motor4(direction):
    if direction == 'forward':
        GPIO.output(RELAY_PIN_MOTOR4, GPIO.HIGH)  # Start motor 4 forward
    elif direction == 'backward':
        GPIO.output(RELAY_PIN_MOTOR4, GPIO.LOW)  # Start motor 4 backward

# Web server route to serve the website
@app.route('/')
def index():
    return render_template('index.html')

# Web server route to provide sensor data
@app.route('/data')
def data():
    global people_count, temperature, humidity, current_station
    return jsonify({'current_station': current_station, 'people_count': people_count, 'temperature': temperature, 'humidity': humidity})

if __name__ == '__main__':
    # Initialize relay pins
    GPIO.setup(RELAY_PIN_MOTOR1, GPIO.OUT)
    GPIO.setup(RELAY_PIN_MOTOR2, GPIO.OUT)
    GPIO.setup(RELAY_PIN_MOTOR3, GPIO.OUT)
    GPIO.setup(RELAY_PIN_MOTOR4, GPIO.OUT)

    # Start threads for counting people, reading sensor data
    count_thread = threading.Thread(target=count_people)
    sensor_thread = threading.Thread(target=read_sensor_data)
    count_thread.start()
    sensor_thread.start()

    # Start Flask web server
    app.run(debug=True, host='0.0.0.0')
