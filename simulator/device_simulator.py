import requests
import time
import random
import numpy as np

# Configuration
API_URL = "http://127.0.0.1:8001/device-data"
DEVICE_ID = "DEV-001"
API_KEY = "secret-api-key"

def simulate_medical_device():
    print(f"Starting Simulator for {DEVICE_ID}...")
    cycle = 0
    
    while True:
        cycle += 1
        
        # Base normal values
        motor_current = random.gauss(2.5, 0.1)
        motor_rpm = random.gauss(3000, 50)
        vibration_level = random.gauss(0.05, 0.005)
        device_temperature = random.gauss(37.0, 0.2)
        battery_voltage = random.gauss(12.0, 0.05)
        error_count = 0
        
        # Introduce degradation after 20 cycles
        if cycle > 20:
            # Gradually increase temperature and vibration
            degradation_factor = (cycle - 20) * 0.1
            device_temperature += degradation_factor
            vibration_level += degradation_factor * 0.01
            motor_current += degradation_factor * 0.05
            
            if cycle > 30:
                error_count = random.randint(1, 3)
        
        payload = {
            "device_id": DEVICE_ID,
            "api_key": API_KEY,
            "motor_current": round(motor_current, 3),
            "motor_rpm": round(motor_rpm, 2),
            "vibration_level": round(vibration_level, 4),
            "device_temperature": round(device_temperature, 2),
            "battery_voltage": round(battery_voltage, 2),
            "error_count": error_count
        }
        
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                result = response.json()
                status = "ANOMALY" if result.get("is_anomaly") else "NORMAL"
                print(f"Cycle {cycle}: Sent data. Status: {status} Score: {result.get('anomaly_score'):.4f}")
            else:
                print(f"Cycle {cycle}: Failed to send data. Status: {response.status_code}")
        except Exception as e:
            print(f"Cycle {cycle}: Connection error: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    simulate_medical_device()
