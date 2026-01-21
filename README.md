Face Recognition Attendance System

An automated attendance management system that uses face recognition to detect employees and log attendance without manual input.

🚀 Features

Real-time face recognition

Automatic attendance marking

Dashboard for attendance insights

Secure and contactless system

CSV export for attendance logs

Flask-based web interface

🧠 Tech Stack

Python

OpenCV

Face Recognition

NumPy

Flask

HTML/CSS

CSV for data persistence

📸 How It Works

Register faces of employees using images

System detects and recognizes faces in real time

Attendance is automatically logged into Attendance.csv

Dashboard displays attendance reports

🗂 Project Structure
📁 EmployeesFaces/       → Stored face images
📁 templates/            → Frontend HTML templates
📄 app.py                → Main recognition logic
📄 dashboard.py          → Dashboard with Flask
📄 Attendance.csv        → Attendance logs
📄 requirements.txt      → Dependencies
🛠 Setup & Installation
1. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   (Mac/Linux)
venv\Scripts\activate      (Windows)
2. Install dependencies
pip install -r requirements.txt
3. Run the application
python app.py
4. Access dashboard

Open browser:

http://localhost:5000
📈 Future Improvements

Cloud storage integration

Employee management UI

Multi-camera support

Role-based admin panel

Integrating databases like MySQL/MongoDB

Author

Khyati Jain

Built as a functional demonstration of integrating computer vision with web technology for automated attendance management.