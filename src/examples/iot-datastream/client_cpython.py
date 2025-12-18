# -----------------------------------------------------------------------------
# MIT License
# 
# Copyright (c) 2025 Mattia Antonini (Fondazione Bruno Kessler) m.antonini@fbk.eu
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------
#
# client_cpython.py - iot-datastream example - CPython Client Side
#        This CPython script simulates an IoT device that sends sensor data
#        to a Flask server using both mPickle and JSON formats.
#

import pickle
import requests
import json
import time
import random

SERVER_URL = "http://localhost:5000/sensor_data"  # Change to your server IP
READING_INTERVAL = 5  # seconds


class SensorReading:
    """Sensor reading data structure"""
    def __init__(self, sensor_type, timestamp, value):
        self.sensor_type = sensor_type
        self.timestamp = timestamp
        self.value = value

    def to_dict(self):
        return {
            'sensor_type': self.sensor_type,
            'timestamp': self.timestamp,
            'value': self.value
        }

def send_with_json(reading, endpoint_url):
    """Serialize with JSON and send to server"""
    print("\n--- Sending with JSON ---")
    
    try:
        # Serialize with JSON
        json_data = json.dumps(reading.to_dict())
        json_size = len(json_data)
        
        # Send to server
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            endpoint_url + '/json',
            data=json_data,
            headers=headers
        )
        
        print(f"JSON size: {json_size} bytes")
        print(f"Response: {response.status_code}")
        print(f"Server message: {response.text}")
        
        response.close()
        return json_size
        
    except Exception as e:
        print(f"Error sending JSON data: {e}")
        return None, None

def send_with_pickle(reading, endpoint_url):
    """Serialize with mPickle and send to server"""
    print("\n--- Sending with mPickle ---")
    
    try:
        # Serialize with pickle
        pickled_data = pickle.dumps(reading)
        pickle_size = len(pickled_data)
        
        # Send to server
        headers = {'Content-Type': 'application/octet-stream'}
        response = requests.post(
            endpoint_url + '/pickle',
            data=pickled_data,
            headers=headers
        )
        
        print(f"Pickle size: {pickle_size} bytes")
        print(f"Response: {response.status_code}")
        print(f"Server message: {response.text}")
        
        response.close()
        return pickle_size
        
    except Exception as e:
        print(f"Error sending pickle data: {e}")
        return None, None


def send_batch_data(readings, endpoint_url):
    """Send multiple readings in a batch using mPickle"""
    print("\n--- Sending batch with mPickle ---")
    
    try:
        # Serialize list of readings
        pickled_batch = pickle.dumps(readings)
        batch_size = len(pickled_batch)
        
        # Send to server
        headers = {'Content-Type': 'application/octet-stream'}
        response = requests.post(
            endpoint_url + '/pickle_batch',
            data=pickled_batch,
            headers=headers
        )
        
        print(f"Batch size: {batch_size} bytes ({len(readings)} readings)")
        print(f"Avg per reading: {batch_size / len(readings):.1f} bytes")
        print(f"Response: {response.status_code}")
        
        response.close()
        return batch_size
        
    except Exception as e:
        print(f"Error sending batch data: {e}")
        return None, None

def collect_sensor_data(sensor_type):
    """Collect data from Random sensor"""
    try:
        # Simulate sensor readings
        if sensor_type.startswith("temperature"):
            value = round(20 + random.uniform(-5, 5), 2)
        elif sensor_type.startswith("humidity"):
            value = round(50 + random.uniform(-20, 20), 2)
        elif sensor_type.startswith("battery"):
            value = round(3.7 + random.uniform(-0.2, 0.2), 2)
        else:
            value = round(20 + random.uniform(-5, 5), 2)
        timestamp = time.time()
        
        reading = SensorReading(
            sensor_type=sensor_type,
            timestamp=timestamp,
            value=value
        )
        
        print(f"Read {sensor_type}: {value}")
        return reading
    
    except Exception as e:
        print(f"Error reading sensor: {e}")
        return None

def main():

    # Uncomment and configure this section to connect to WiFi on a MicroPython device
    # import network
    # # enable station interface and connect to WiFi access point
    # nic = network.WLAN(network.WLAN.IF_STA)
    # nic.active(True)
    # nic.connect(WIFI_SSID, WIFI_PASSWORD)

    print("\n=== mPickle Datastream Example ===\n")
    print("Running on CPython environment")

    print("Sending IoT sensor data to server at", SERVER_URL)


    # Storage for batch sending
    batch_readings = []
    batch_size = 5
    
    print(f"\nStarting data collection (every {READING_INTERVAL}s)")
    print("Press Ctrl+C to stop\n")
    
    iteration = 0
    
    try:
        while True:
            iteration += 1
            print(f"\n{'=' * 50}")
            print(f"Iteration {iteration}")
            print(f"{'=' * 50}")
            
            # Collect sensor data
            readings = [
                collect_sensor_data("temperature_cpython"),
                collect_sensor_data("humidity_cpython"),
                collect_sensor_data("battery_cpython")
            ]
            
            for reading in readings:
                if reading:
                    # Send individual reading
                    pickle_size = send_with_pickle(reading, SERVER_URL)
                    json_size = send_with_json(reading, SERVER_URL)
                
                    # Compare efficiency
                    if pickle_size and json_size:
                        print(f"\nComparison:")
                        print(f"  Pickle: {pickle_size} bytes")
                        print(f"  JSON:   {json_size} bytes")
                        print(f"  Pickle is {((json_size - pickle_size) / json_size * 100):.1f}% smaller")
                
                # Add to batch
                batch_readings.append(reading)
                
                # Send batch when ready
                if len(batch_readings) >= batch_size:
                    send_batch_data(batch_readings, SERVER_URL)
                    batch_readings = []
            
            # Show memory status
            
            # Wait for next reading
            time.sleep(READING_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\nStopping...")
        # Send remaining batch data
        if batch_readings:
            print("Sending remaining batch data...")
            send_batch_data(batch_readings, SERVER_URL)
    

if __name__ == "__main__":
    main()
