📚 Face Detection Attendance System

This project is a real-time Face Detection Attendance System built using a laptop webcam. The idea is to automate attendance capture without relying on manual input, RFID cards, or QR codes. The system detects faces in real time, logs a timestamp for detected individuals, and shows attendance records through a simple dashboard.

The focus of this build is on creating a working offline pipeline using practical computer vision techniques that work on normal hardware.

🎯 Objectives

Detect human faces using a normal laptop camera

Capture attendance automatically upon detection

Maintain offline operation for privacy & reliability

Provide a dashboard for viewing captured attendance logs

Keep system lightweight and usable without special hardware

🧠 How the System Works

The laptop webcam captures live frames using OpenCV

Faces in the frame are detected using a dlib-based detection model

When a new face is detected, the system logs an entry as "DetectedFace" along with a timestamp

A Flask dashboard displays attendance records in a readable format

The system ensures that the same face is not logged repeatedly during continuous presence

This serves as a strong foundation for later adding identity recognition.

🗂 Project Structure
Attendance-System/
│
├── Code.py                # Main face detection + attendance logging
├── Code_lite.py           # Lightweight testing version
├── flask_dashboard.py     # Dashboard backend
├── templates/             # HTML templates for dashboard UI
├── EmployeesFaces/        # Face dataset (for future recognition)
├── Attendance.csv         # Attendance log file
├── requirements.txt       # Dependencies
└── README.md              # Documentation

⚙️ Tech Stack

Language: Python
Computer Vision: OpenCV, dlib
Backend Framework: Flask
Data Storage: CSV
Frontend: HTML (via Flask templates)
Hardware: Laptop webcam
Execution: Offline (no internet required)

🏁 How to Run the Project
1. Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate         # Linux/Mac
venv\Scripts\activate            # Windows

2. Install dependencies
pip install -r requirements.txt

3. Run the detection system
python Code.py


This opens the webcam and begins detection.

4. Launch the dashboard
python flask_dashboard.py


Open browser at:

http://localhost:5000

📒 Attendance Logging Logic

For each new face detected:

(DetectedFace, Date, Time)


Example log entry:

DetectedFace, 2026-01-20, 10:42:13


The system checks existing logs to avoid writing duplicates for continuous presence in front of the camera.

🧩 Use Cases

This type of system can be used in:

✔ Classrooms / Training centers
✔ Workspaces / Offices
✔ Co-working spaces
✔ Event check-in scenarios
✔ Access-controlled environments

🚧 Current Limitations (For this Iteration)

To keep the build focused and stable:

Identity recognition (mapping faces to names) is not yet implemented

System currently logs only "DetectedFace"

Multi-person tracking in the same frame is not included

No entry/exit direction detection yet

No movement-based re-identification logic

Dashboard is local-only (not cloud deployed)

These features require more advanced tracking, embedding management, and state logic.

🚀 Future Improvements (Planned Roadmap)

Next iterations can include:

Naming/identity recognition using facial embeddings comparison

SVM/KNN classifier on embeddings for stronger identity matching

YOLO + DeepSORT for multi-person tracking

Entry/exit direction classification

Re-identification across sessions

Database integration (MySQL/Postgres)

Analytics dashboard (graphs, stats, summaries)

Web/mobile admin panel

Cloud deployment and remote monitoring

This roadmap aligns with scalable product deployment.

🔐 Why Offline?

Computer vision attendance systems are commonly deployed offline due to:

Privacy (face data does not leave device)

Lower inference latency

No internet dependency for operation

Fits on-premise enterprise setups

This mirrors how many real attendance systems are deployed in offices.

👨‍💻 Author

Khyati Jain
Computer Science Engineering Student
