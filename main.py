
# final final code

import cv2
import pandas as pd
import numpy as np
import os
import streamlit as st
import time

# Initialize session state
if "scanner_running" not in st.session_state:
    st.session_state.scanner_running = True  # Start scanner by default
if "last_scan_time" not in st.session_state:
    st.session_state.last_scan_time = 0

# Function to save data to CSV
def save_to_csv(data):
    file_path = "qr_codes.csv"
    new_data = pd.DataFrame({'QR Code Data': [data]})

    # Check if the file exists and is not empty
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            df = pd.read_csv(file_path)
            if data not in df['QR Code Data'].values:
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(file_path, index=False)
                return "Attendance marked successfully."
            else:
                return "Duplicate QR Code Data. Attendance already marked."
        except pd.errors.EmptyDataError:
            new_data.to_csv(file_path, index=False)
            return "Attendance marked successfully."
    else:
        # If the file does not exist or is empty, create it with the new data
        new_data.to_csv(file_path, index=False)
        return "Attendance marked successfully."

# QR code scanner function
def scan_qr_code():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 30)

    st.title("QR Code Scanner for ENGINEERING UNPLUGGED")
    st.write("Organized by Abhivriddhi - Student Training Committee, VIT Pune.")
    st.write("Designed By - Managment Team, Abhivriddhi")

    # Initialize the QRCodeDetector
    detector = cv2.QRCodeDetector()

    # Create an empty placeholder for the video feed
    frame_placeholder = st.empty()

    # Create a placeholder for the status message
    status_placeholder = st.empty()

    while st.session_state.scanner_running:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to grab frame.")
            break

        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # Decode the QR code
        data, bbox, _ = detector.detectAndDecode(frame)

        current_time = time.time()
        if data and current_time - st.session_state.last_scan_time > 3:  # 3-second delay between scans
            st.session_state.last_scan_time = current_time
            status_message = save_to_csv(data)
            status_placeholder.success(f"QR Code Data: {data}\n{status_message}")

            # Draw bounding box
            if bbox is not None and len(bbox) > 0:
                pts = np.int32(bbox).reshape(-1, 2)
                cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

            # Clear the status message after 2 seconds
            time.sleep(2)
            status_placeholder.empty()

        # Convert the frame to RGB format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)

    cap.release()

# Display header image
st.image("header_image.png", use_column_width=True)

# Start the QR code scanner automatically
scan_qr_code()


