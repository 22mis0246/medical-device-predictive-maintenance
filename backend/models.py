from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from .database import Base
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- SQLAlchemy Models ---

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # admin, technician, viewer

class Device(Base):
    __tablename__ = "devices"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    api_key = Column(String, unique=True)
    status = Column(String, default="active")

class SensorData(Base):
    __tablename__ = "sensor_data"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.id"))
    motor_current = Column(Float)
    motor_rpm = Column(Float)
    vibration_level = Column(Float)
    device_temperature = Column(Float)
    battery_voltage = Column(Float)
    error_count = Column(Integer)
    anomaly_score = Column(Float)
    is_anomaly = Column(Integer)  # 0 or 1
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.id"))
    message = Column(Text)
    severity = Column(String)
    is_resolved = Column(Integer, default=0)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    details = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

# --- Pydantic Schemas ---

class DeviceDataIn(BaseModel):
    device_id: str
    api_key: str
    motor_current: float
    motor_rpm: float
    vibration_level: float
    device_temperature: float
    battery_voltage: float
    error_count: int

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
