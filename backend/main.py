import sys
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import joblib
import pandas as pd

# Standard import style for absolute imports
from .database import engine, get_db, Base
from .models import User, Device, SensorData, Alert, AuditLog, DeviceDataIn, UserCreate, UserOut, Token
from .auth import get_password_hash, verify_password, create_access_token, get_current_user, check_admin_role, check_technician_role

# Initialize Database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Medical Device Predictive Maintenance System")

# Load ML Model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "anomaly_model.pkl")
model = None
try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")

def log_audit(db: Session, user_id: int, action: str, details: str):
    audit_entry = AuditLog(user_id=user_id, action=action, details=details)
    db.add(audit_entry)
    db.commit()

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    db = next(get_db())
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            hashed_pw = get_password_hash("admin123")
            new_admin = User(username="admin", hashed_password=hashed_pw, role="admin")
            db.add(new_admin)
            db.commit()
        
        device = db.query(Device).filter(Device.id == "DEV-001").first()
        if not device:
            new_device = Device(id="DEV-001", name="Ventilator-X1", api_key="secret-api-key")
            db.add(new_device)
            db.commit()
    finally:
        db.close()
    
    yield
    # Shutdown logic (if any)

app = FastAPI(title="Medical Device Predictive Maintenance System", lifespan=lifespan)

@app.post("/token", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    log_audit(db, user.id, "LOGIN", f"User {user.username} logged in")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/device-data")
async def receive_device_data(data: DeviceDataIn, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == data.device_id, Device.api_key == data.api_key).first()
    if not device:
        raise HTTPException(status_code=401, detail="Invalid Device ID or API Key")
    
    feature_names = ['motor_current', 'motor_rpm', 'vibration_level', 'device_temperature', 'battery_voltage', 'error_count']
    input_data = data.model_dump(include=set(feature_names)) if hasattr(data, "model_dump") else data.dict(include=set(feature_names))
    input_df = pd.DataFrame([input_data])
    
    is_anomaly = 0
    anomaly_score = 0.0
    if model:
        prediction = model.predict(input_df)[0]
        anomaly_score = float(model.decision_function(input_df)[0])
        is_anomaly = 1 if prediction == -1 else 0
    
    sensor_entry = SensorData(device_id=data.device_id, **input_data, anomaly_score=anomaly_score, is_anomaly=is_anomaly)
    db.add(sensor_entry)
    
    if is_anomaly:
        alert = Alert(device_id=data.device_id, message=f"Anomaly detected! Score: {anomaly_score:.4f}", severity="High")
        db.add(alert)
    
    db.commit()
    return {"status": "success", "is_anomaly": bool(is_anomaly), "anomaly_score": anomaly_score}

@app.get("/alerts")
async def get_alerts(db: Session = Depends(get_db), current_user: User = Depends(check_technician_role)):
    return db.query(Alert).order_by(Alert.timestamp.desc()).limit(50).all()

@app.get("/device-status/{device_id}")
async def get_device_status(device_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    latest_data = db.query(SensorData).filter(SensorData.device_id == device_id).order_by(SensorData.timestamp.desc()).first()
    if not latest_data:
        raise HTTPException(status_code=404, detail="No data found for this device")
    return latest_data

@app.get("/audit-logs")
async def get_audit_logs(db: Session = Depends(get_db), current_user: User = Depends(check_admin_role)):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()
