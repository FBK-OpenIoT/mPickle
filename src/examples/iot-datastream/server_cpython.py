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
# server_cpython.py - iot-datastream example - Python Server Side (CPython)
#           This Flask server receives sensor data from ESP32 devices using both
#           mPickle and JSON formats. It stores the data.
#           and provides visualization. Then configure your MicroPython device to
#           send data to http://YOUR_IP:5000/sensor_data
#        Requirements:  pip install flask pickle matplotlib pandas
#        Usage:         python server.py


from flask import Flask, request, jsonify
import pickle
import json
from datetime import datetime
import threading
import time
from collections import defaultdict

app = Flask(__name__)

# Data storage
sensor_data = defaultdict(list)
data_lock = threading.Lock()

# Statistics
stats = {
    'pickle_requests': 0,
    'json_requests': 0,
    'pickle_bytes': 0,
    'json_bytes': 0,
    'total_readings': 0
}

class SensorReading:
    """Sensor reading data structure"""
    def __init__(self, sensor_type, timestamp, value):
        self.sensor_type = sensor_type
        self.timestamp = timestamp
        self.value = value
    
    def __repr__(self):
        dt = datetime.fromtimestamp(self.timestamp)
        return (f"SensorReading(type={self.sensor_type}, "
                f"time={dt.strftime('%H:%M:%S')}, "
                f"value={self.value})")
    
    def to_dict(self):
        return {
            'sensor_type': self.sensor_type,
            'timestamp': self.timestamp,
            'datetime': datetime.fromtimestamp(self.timestamp).isoformat(),
            'value': self.value
        }

@app.route('/')
def index():
    """IoT Datastream Example - Server status page"""
    return """
    <html>
    <head><title>IoT Datastream Example - Server</title></head>
    <body>
        <h1>IoT Datastream Example - Server</h1>
        <h2>Status: Running ✓</h2>
        <h3>Statistics:</h3>
        <ul>
            <li>Total readings: {total}</li>
            <li>Pickle requests: {pickle_req} ({pickle_bytes} bytes)</li>
            <li>JSON requests: {json_req} ({json_bytes} bytes)</li>
            <li>Active sensors: {sensors}</li>
        </ul>
        <h3>Endpoints:</h3>
        <ul>
            <li>POST /sensor_data/pickle - Receive pickled sensor data</li>
            <li>POST /sensor_data/json - Receive JSON sensor data</li>
            <li>POST /sensor_data/pickle_batch - Receive batch of pickled data</li>
            <li>GET <a href="/sensor_data"> /sensor_data - Get all sensor data</a></li>
            <li>GET <a href="/stats"> /stats - Get server statistics</a></li>
        </ul>
    </body>
    </html>
    """.format(
        total=stats['total_readings'],
        pickle_req=stats['pickle_requests'],
        pickle_bytes=stats['pickle_bytes'],
        json_req=stats['json_requests'],
        json_bytes=stats['json_bytes'],
        sensors=len(sensor_data)
    )

@app.route('/sensor_data/pickle', methods=['POST'])
def receive_pickle():
    """Receive pickled sensor data"""
    try:
        # Get binary data
        pickled_data = request.data
        data_size = len(pickled_data)
        
        # Deserialize
        reading = pickle.loads(pickled_data)
        
        # Store data
        with data_lock:
            sensor_data[reading.sensor_type].append(reading)
            stats['pickle_requests'] += 1
            stats['pickle_bytes'] += data_size
            stats['total_readings'] += 1
        
        print(f"[PICKLE] Received: {reading}")
        print(f"         Size: {data_size} bytes")
        
        return jsonify({
            'status': 'success',
            'message': f'Pickle data received: {data_size} bytes',
            'reading': reading.to_dict()
        }), 200
        
    except Exception as e:
        print(f"Error processing pickle data: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/sensor_data/json', methods=['POST'])
def receive_json():
    """Receive JSON sensor data"""
    try:
        # Get JSON data
        json_data = request.data
        data_size = len(json_data)
        data_dict = json.loads(json_data)
        
        # Create SensorReading object
        reading = SensorReading(
            sensor_type=data_dict['sensor_type'],
            timestamp=data_dict['timestamp'],
            value=data_dict['value']
        )
        
        # Store data
        with data_lock:
            sensor_data[reading.sensor_type].append(reading)
            stats['json_requests'] += 1
            stats['json_bytes'] += data_size
            stats['total_readings'] += 1
        
        print(f"[JSON] Received: {reading}")
        print(f"       Size: {data_size} bytes")
        
        return jsonify({
            'status': 'success',
            'message': f'JSON data received: {data_size} bytes',
            'reading': reading.to_dict()
        }), 200
        
    except Exception as e:
        print(f"Error processing JSON data: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/sensor_data/pickle_batch', methods=['POST'])
def receive_pickle_batch():
    """Receive batch of pickled sensor data"""
    try:
        # Get binary data
        pickled_data = request.data
        data_size = len(pickled_data)
        
        # Deserialize batch
        readings = pickle.loads(pickled_data)
        
        # Store all readings
        with data_lock:
            for reading in readings:
                sensor_data[reading.sensor_type].append(reading)
            stats['pickle_requests'] += 1
            stats['pickle_bytes'] += data_size
            stats['total_readings'] += len(readings)
        
        print(f"[PICKLE BATCH] Received: {len(readings)} readings")
        print(f"               Size: {data_size} bytes ({data_size/len(readings):.1f} bytes/reading)")
        
        return jsonify({
            'status': 'success',
            'message': f'Batch received: {len(readings)} readings, {data_size} bytes',
            'count': len(readings)
        }), 200
        
    except Exception as e:
        print(f"Error processing pickle batch: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/sensor_data', methods=['GET'])
def get_all_data():
    """Get all sensor data"""
    with data_lock:
        result = {}
        for sensor_type, readings in sensor_data.items():
            result[sensor_type] = [r.to_dict() for r in readings]
        return jsonify(result), 200

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get server statistics"""
    with data_lock:
        detailed_stats = dict(stats)
        detailed_stats['sensors'] = {}
        
        for sensor_type, readings in sensor_data.items():
            if readings:
                detailed_stats['sensors'][sensor_type] = {
                    'count': len(readings),
                    'first_reading': readings[0].to_dict(),
                    'last_reading': readings[-1].to_dict()
                }
        
        # Calculate efficiency
        if stats['pickle_bytes'] > 0 and stats['json_bytes'] > 0:
            detailed_stats['pickle_efficiency'] = {
                'bytes_saved': stats['json_bytes'] - stats['pickle_bytes'],
                'percent_smaller': ((stats['json_bytes'] - stats['pickle_bytes']) / stats['json_bytes'] * 100)
            }
        
        return jsonify(detailed_stats), 200

def print_summary():
    """Print periodic summary"""
    while True:
        time.sleep(60)  # Every minute
        with data_lock:
            if stats['total_readings'] > 0:
                print("\n" + "="*60)
                print("SUMMARY")
                print("="*60)
                print(f"Total readings: {stats['total_readings']}")
                print(f"Pickle: {stats['pickle_requests']} requests, {stats['pickle_bytes']} bytes")
                print(f"JSON: {stats['json_requests']} requests, {stats['json_bytes']} bytes")
                
                if stats['pickle_bytes'] > 0 and stats['json_bytes'] > 0:
                    savings = ((stats['json_bytes'] - stats['pickle_bytes']) / stats['json_bytes'] * 100)
                    print(f"Pickle is {savings:.1f}% more efficient")
                
                print(f"Active sensors: {len(sensor_data)}")
                for sensor_type, readings in sensor_data.items():
                    print(f"  - {sensor_type}: {len(readings)} readings")
                print("="*60 + "\n")

def save_to_csv():
    """Save data to CSV files periodically"""
    import pandas as pd
    
    while True:
        time.sleep(300)  # Every 5 minutes
        with data_lock:
            if sensor_data:
                for sensor_type, readings in sensor_data.items():
                    if readings:
                        df = pd.DataFrame([r.to_dict() for r in readings])
                        filename = f"sensor_data_{sensor_type}_{datetime.now().strftime('%Y%m%d')}.csv"
                        df.to_csv(filename, index=False)
                        print(f"Saved {len(readings)} readings to {filename}")

def main():
    """Main function"""
    print("="*60)
    print("IoT Sensor Data Server")
    print("="*60)
    print("Starting server on http://0.0.0.0:5000")
    print("Endpoints:")
    print("  POST /sensor_data/pickle - Receive pickled data")
    print("  POST /sensor_data/json - Receive JSON data")
    print("  POST /sensor_data/pickle_batch - Receive batch data")
    print("  GET /sensor_data - Get all data")
    print("  GET /stats - Get statistics")
    print("="*60 + "\n")
    
    # Start background threads
    summary_thread = threading.Thread(target=print_summary, daemon=True)
    summary_thread.start()
    
    # Uncomment to enable CSV saving
    # csv_thread = threading.Thread(target=save_to_csv, daemon=True)
    # csv_thread.start()
    
    # Start Flask server
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    main()
