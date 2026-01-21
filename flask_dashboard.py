"""
Flask Dashboard for Attendance System
Runs in a separate thread alongside the main recognition loop
"""

import threading
import cv2
import json
import os
from datetime import datetime
from flask import Flask, render_template, Response, jsonify
from pathlib import Path
import queue

app = Flask(__name__)


class DashboardData:
    def __init__(self):
        self.current_frame = None
        self.current_users = set()
        self.lock = threading.Lock()
        self.csv_path = 'Attendance.csv'
    
    def update_frame(self, frame):
        """Thread-safe frame update"""
        with self.lock:
            self.current_frame = frame.copy() if frame is not None else None
    
    def update_active_users(self, users_set):
        """Thread-safe active users update"""
        with self.lock:
            self.current_users = users_set.copy()
    
    def get_frame(self):
        """Thread-safe frame retrieval"""
        with self.lock:
            return self.current_frame.copy() if self.current_frame is not None else None
    
    def get_active_users(self):
        """Thread-safe active users retrieval"""
        with self.lock:
            return list(self.current_users)

dashboard_data = DashboardData()

def generate_frames():
    """Generator for MJPEG video stream"""
    while True:
        frame = dashboard_data.get_frame()
        if frame is None:
            continue
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n'
               b'Content-Length: ' + str(len(frame_bytes)).encode() + b'\r\n\r\n' +
               frame_bytes + b'\r\n')

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """MJPEG video stream endpoint"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/attendance')
def get_attendance():
    """Return attendance records as JSON"""
    csv_path = dashboard_data.csv_path
    records = []
    
    if os.path.exists(csv_path):
        try:
            with open(csv_path, 'r') as f:
                lines = f.readlines()
                
            # Skip header
            for line in lines[1:]:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    records.append({
                        'name': parts[0],
                        'time': parts[1],
                        'date': parts[2]
                    })
        except Exception as e:
            print(f"Error reading attendance: {e}")
    
    return jsonify(records)

@app.route('/active')
def get_active():
    """Return currently active users"""
    users = dashboard_data.get_active_users()
    today = datetime.now().strftime('%Y-%m-%d')
    
    total_today = 0
    csv_path = dashboard_data.csv_path
    if os.path.exists(csv_path):
        try:
            with open(csv_path, 'r') as f:
                lines = f.readlines()
            
            for line in lines[1:]:
                parts = line.strip().split(',')
                if len(parts) >= 3 and parts[2] == today:
                    total_today += 1
        except:
            pass
    
    return jsonify({
        'active_now': users,
        'count_active': len(users),
        'total_today': total_today
    })

@app.route('/stats')
def get_stats():
    """Return analytics stats"""
    today = datetime.now().strftime('%Y-%m-%d')
    total_today = 0
    unique_people = set()
    
    csv_path = dashboard_data.csv_path
    if os.path.exists(csv_path):
        try:
            with open(csv_path, 'r') as f:
                lines = f.readlines()
            
            for line in lines[1:]:
                parts = line.strip().split(',')
                if len(parts) >= 3 and parts[2] == today:
                    total_today += 1
                    unique_people.add(parts[0])
        except:
            pass
    
    active = dashboard_data.get_active_users()
    
    return jsonify({
        'total_marked': len(unique_people),
        'total_entries': total_today,
        'active_now': len(active),
        'date': today
    })

def run_flask(port=5000):
    """Run Flask server (call this in a separate thread)"""
    app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False, threaded=True)

def start_dashboard_server(port=5000):
    """Start dashboard server in a separate daemon thread"""
    flask_thread = threading.Thread(target=run_flask, args=(port,), daemon=True)
    flask_thread.start()
    print(f"Dashboard server started on http://127.0.0.1:{port}")
    return flask_thread
