# medical-device-predictive-maintenance
Medical Device Predictive Maintenance System that uses machine learning (Isolation Forest) to detect anomalies from real-time device sensor data. Built with FastAPI, PostgreSQL, and Streamlit for live monitoring, alert generation, and role-based authentication.

# 🏥 Medical Device Predictive Maintenance System

A full-stack predictive maintenance platform that monitors medical device sensor data in real-time and detects anomalies using Machine Learning.

The system simulates device data, performs anomaly detection using Isolation Forest, stores results in PostgreSQL, and provides a live monitoring dashboard with secure authentication.

---

## 🚀 Features

- 🔐 JWT-based Authentication (Admin / Technician roles)
- 📊 Real-time Device Monitoring Dashboard (Streamlit)
- 🤖 Machine Learning Anomaly Detection (Isolation Forest)
- 🗄 PostgreSQL Database Integration
- ⚡ FastAPI Backend with Swagger Documentation
- 🔄 Live Device Data Simulation
- 🚨 Automatic Alert Generation for Critical Conditions

---

## 🏗 System Architecture

Device Simulator  
⬇  
FastAPI Backend (ML + Auth + DB)  
⬇  
PostgreSQL Database  
⬇  
Streamlit Dashboard  

---

## 🛠 Tech Stack

**Backend:** FastAPI, SQLAlchemy  
**Database:** PostgreSQL  
**Machine Learning:** Scikit-learn (Isolation Forest)  
**Frontend:** Streamlit  
**Authentication:** JWT, Passlib (bcrypt)  
**Simulation:** Python  

---

## 📂 Project Structure


medical-device-predictive-system/
│
├── backend/ # FastAPI backend (APIs, ML, Auth)
├── simulator/ # Device data simulator
├── dashboard/ # Streamlit monitoring dashboard
├── models/ # Trained ML model
├── venv/ # Virtual environment (ignored)
└── requirements.txt


---

## ⚙️ How to Run the Project

### 1️⃣ Activate Virtual Environment


venv\Scripts\activate


### 2️⃣ Start Backend


uvicorn backend.main:app --reload --port 8001


### 3️⃣ Start Device Simulator (New Terminal)


python simulator/device_simulator.py


### 4️⃣ Start Dashboard (New Terminal)


streamlit run dashboard/app.py


Open:

http://localhost:8501


---


---

## 🤖 How Anomaly Detection Works

The system uses **Isolation Forest**, an unsupervised anomaly detection algorithm.  
It learns normal device behavior and flags unusual sensor patterns as anomalies.

When an anomaly is detected:
- An alert is generated
- Device status changes to CRITICAL
- Event is stored in the database

---

## 📈 Future Improvements

- Cloud deployment (AWS / Azure / GCP)
- Email/SMS alert notifications
- Time-series database integration
- Model retraining pipeline
- Real IoT hardware integration

---

## 📜 License

This project is for educational and research purposes.
