@echo off
echo ==========================================
echo Medical Device System Setup ^& Launcher
echo ==========================================

echo [1/4] Installing dependencies...
pip install -r requirements.txt

echo [2/4] Training anomaly detection model...
python models/train_model.py

echo [3/4] Starting Backend API in new window...
start cmd /k "uvicorn backend.main:app --host 0.0.0.0 --port 8000"

echo [4/4] Starting Dashboard in new window...
start cmd /k "streamlit run dashboard/app.py"

echo.
echo ==========================================
echo System is starting up!
echo - API: http://localhost:8000
echo - Dashboard: http://localhost:8501
echo - Admin: admin / admin123
echo ==========================================
echo.
echo To start the device simulator, run: python simulator/device_simulator.py
pause
