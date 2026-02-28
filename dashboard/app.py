import streamlit as st
import requests
import pandas as pd
import time
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Medical Device Health Dashboard", layout="wide")

API_BASE_URL = "http://127.0.0.1:8001"

# Session State for Authentication
if 'token' not in st.session_state:
    st.session_state['token'] = None
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None

def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        try:
            response = requests.post(f"{API_BASE_URL}/token", data={"username": username, "password": password})
            if response.status_code == 200:
                data = response.json()
                st.session_state['token'] = data['access_token']
                # Decode role from JWT or just use hardcoded for demo if API doesn't return it
                # For this demo, let's assume 'admin' is admin
                st.session_state['user_role'] = 'admin' if username == 'admin' else 'viewer'
                st.sidebar.success("Logged in!")
                st.rerun()
            else:
                st.sidebar.error("Invalid credentials")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

def dashboard():
    st.title("🏥 Medical Device Predictive Maintenance")
    
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    
    # 1. Real-time Status
    st.subheader("Current Device Status - DEV-001")
    try:
        resp = requests.get(f"{API_BASE_URL}/device-status/DEV-001", headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Temperature", f"{data['device_temperature']} °C", delta_color="inverse")
            col2.metric("Vibration", f"{data['vibration_level']} g")
            col3.metric("Battery", f"{data['battery_voltage']} V")
            
            health_status = "Healthy" if not data['is_anomaly'] else "CRITICAL"
            color = "green" if health_status == "Healthy" else "red"
            col4.markdown(f"Status: **:{color}[{health_status}]**")
        else:
            st.warning("No live data available yet. Start the simulator.")
    except Exception as e:
        st.error(f"Backend unreachable: {e}")

    # 2. Alert History
    st.divider()
    st.subheader("🔔 Recent Alerts")
    try:
        resp = requests.get(f"{API_BASE_URL}/alerts", headers=headers)
        if resp.status_code == 200:
            alerts = resp.json()
            if alerts:
                df_alerts = pd.DataFrame(alerts)
                st.table(df_alerts[['timestamp', 'message', 'severity']])
            else:
                st.info("No alerts detected.")
    except:
        pass

    # 3. Audit Logs (Admin Only)
    if st.session_state['user_role'] == 'admin':
        st.divider()
        st.subheader("📜 System Audit Logs")
        try:
            resp = requests.get(f"{API_BASE_URL}/audit-logs", headers=headers)
            if resp.status_code == 200:
                logs = resp.json()
                st.write(pd.DataFrame(logs))
        except:
            pass

    if st.button("Logout"):
        st.session_state['token'] = None
        st.rerun()

# Main App Flow
if not st.session_state['token']:
    st.info("Please log in from the sidebar to access the dashboard.")
    login()
else:
    dashboard()
    time.sleep(2)
    st.rerun()
    
