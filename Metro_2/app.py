import RPi.GPIO as GPIO
import time
from flask import Flask, render_template, jsonify
import threading

app = Flask(__name__)

# Ultrasonic sensor setup
TRIG = 23
ECHO = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Flame sensor GPIO pin
FLAME_SENSOR_PIN = 4  # GPIO pin connected to the flame sensor

# L298N motor driver GPIO pins
# Replace these with the actual GPIO pins connected to your L298N motor driver
IN1 = 17  # Input 1 pin for motor A
IN2 = 27  # Input 2 pin for motor A
IN3 = 22  # Input 3 pin for motor B
IN4 = 10  # Input 4 pin for motor B

# Buzzer GPIO pin
BUZZER_PIN = 25  # GPIO pin for the buzzer

# Global variables
people_count = 0
current_station = 1  # Initialize current station to 1
stations = {1: "Chattrapati Shivaji Terminal (CST)", 2: "Grand Central Terminal (GCT)", 3: "Dadar Railway Station (DRT)", 4: "Terminus"}

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

# Function to control motors for moving forward or backward
def control_motors(direction):
    if direction == 'forward':
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
    elif direction == 'backward':
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)

# Function to stop motors
def stop_motors():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

# Function to move the metro forward to the next station
def move_forward():
    global current_station
    current_station = (current_station % len(stations)) + 1
    control_motors('forward')
    time.sleep(5)  # Adjust this value according to the time taken to reach the next station
    stop_motors()

# Function to move the metro backward to start again from the first station
def move_backward():
    global current_station
    current_station = 1  # Reset to the first station
    control_motors('backward')
    time.sleep(20)  # Adjust this value according to the time taken to reverse to the first station
    stop_motors()

# Main loop for metro movement
def metro_movement_loop():
    while True:
        move_forward()  # Move forward to the next station
        if current_station == len(stations):  # If it reaches the last station, move backward
            move_backward()

# Web server route to serve the website
@app.route('/')
def index():
    next_station = (current_station % len(stations)) + 1
    return render_template('index.html', current_station=stations[current_station], next_station=stations[next_station])

# Web server route to provide sensor data
@app.route('/data')
def data():
    global people_count, current_station
    return jsonify({'current_station': stations[current_station], 'people_count': people_count})

if __name__ == '__main__':
    # Start the metro movement loop in a separate thread
    movement_thread = threading.Thread(target=metro_movement_loop)
    movement_thread.start()

    # Start the Flask web server
    app.run(debug=True, host='0.0.0.0')
