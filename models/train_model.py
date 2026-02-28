import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

def generate_synthetic_data(n_samples=1000):
    """Generates synthetic normal operating data for a medical device."""
    np.random.seed(42)
    
    data = {
        'motor_current': np.random.normal(2.5, 0.2, n_samples),
        'motor_rpm': np.random.normal(3000, 100, n_samples),
        'vibration_level': np.random.normal(0.05, 0.01, n_samples),
        'device_temperature': np.random.normal(37.0, 0.5, n_samples),
        'battery_voltage': np.random.normal(12.0, 0.1, n_samples),
        'error_count': np.random.poisson(0.1, n_samples)
    }
    
    return pd.DataFrame(data)

def train_and_save_model():
    """Trains an Isolation Forest model and saves it."""
    print("Generating synthetic data...")
    df = generate_synthetic_data()
    
    print("Training Isolation Forest model...")
    # contamination is the expected proportion of outliers in the data
    model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    model.fit(df)
    
    model_path = os.path.join(os.path.dirname(__file__), 'anomaly_model.pkl')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_and_save_model()
