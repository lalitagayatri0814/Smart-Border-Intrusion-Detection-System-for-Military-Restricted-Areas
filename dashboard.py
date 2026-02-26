import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import time
import os

# Page config
st.set_page_config(page_title="Restricted Area Intrusion Detection", layout="wide")
st.title("🔐 Restricted Area Intrusion Detection System")

# -------------------- EMAIL FUNCTION --------------------
def send_email_alert(zone, motion, vibration):
    sender = "arya70753352@gmail.com"        # replace with your Gmail
    receiver = "jasvidurgacse.genai@gmail.com"  # replace with receiver
    password = "egnk gcer rtgv ocpz"         # Gmail App Password
    subject = "🚨 Intrusion Alert Detected!"
    body = f"""
ALERT DETECTED!

Zone: {zone}
Motion: {motion}
Vibration: {vibration}
Time: {datetime.now()}
"""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        st.info(f"📧 Email alert sent for {zone}")
    except Exception as e:
        st.warning(f"Failed to send email: {e}")

# -------------------- FILE CHECK --------------------
output_file = "output.csv"
if not os.path.exists(output_file):
    pd.DataFrame(columns=["timestamp", "zone", "motion", "vibration", "anomaly"]).to_csv(output_file, index=False)

# -------------------- STREAMLIT PLACEHOLDERS --------------------
placeholder_table = st.empty()
placeholder_chart = st.empty()
placeholder_alert = st.empty()

# Select zone for chart (unique key)
selected_zone = st.selectbox("Select Zone for Graph", options=["Border","Warehouse","ControlRoom"], key="zone_select")

# -------------------- MAIN LOOP --------------------
while True:
    try:
        # Read sensor data
        if not os.path.exists("sensor_data.csv"):
            st.warning("Waiting for sensor_data.csv file...")
            time.sleep(2)
            continue

        data = pd.read_csv("sensor_data.csv")
        if data.empty:
            st.warning("No sensor data yet...")
            time.sleep(2)
            continue

        data['timestamp'] = pd.to_datetime(data['timestamp'])

        # Calculate anomaly
        def check_anomaly(row):
            current_hour = datetime.now().hour
            zone = row['zone']
            motion = row['motion']
            vibration = row['vibration']

            # Zone-based threshold
            if zone == "Border":
                threshold = 5
            elif zone == "Warehouse":
                threshold = 10
            else:
                threshold = 8

            # Time-based logic: allowed 9AM-5PM
            if motion > threshold or vibration > threshold:
                return True
            elif current_hour < 9 or current_hour > 17:
                if motion > 5:
                    return True
            return False

        data['anomaly'] = data.apply(check_anomaly, axis=1)
        data.to_csv(output_file, index=False)

        # Display latest 10 rows
        placeholder_table.dataframe(data.tail(10))

        # -------------------- ALERT --------------------
        anomalies = data[data['anomaly'] == True]
        if not anomalies.empty:
            latest = anomalies.tail(1).iloc[0]
            zone = latest['zone']
            motion = latest['motion']
            vibration = latest['vibration']
            placeholder_alert.error(f"⚠️ ALERT! Zone: {zone}, Motion: {motion}, Vibration: {vibration}")
            send_email_alert(zone, motion, vibration)
        else:
            placeholder_alert.success("✅ All zones secure")

        # -------------------- LIVE CHART --------------------
        filtered = data[data['zone'] == selected_zone]
        placeholder_chart.subheader(f"📊 Live Sensor Trends - {selected_zone}")
        placeholder_chart.line_chart(filtered.set_index("timestamp")[["motion","vibration"]])

        # Wait 2 seconds before refreshing
        time.sleep(2)

    except Exception as e:
        st.warning(f"Waiting for data... {e}")
        time.sleep(2)