import cv2
import numpy as np
import os
from datetime import datetime
import pyttsx3
import tkinter as tk
from tkinter import simpledialog


engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


path = 'EmployeesFaces'
if not os.path.exists(path):
    os.makedirs(path)

marked_today_set = set()

def load_today_attendance():
    file_path = 'Attendance.csv'
    if not os.path.exists(file_path):
        return

    now = datetime.now()
    dateString = now.strftime('%Y-%m-%d')
    
    with open(file_path, 'r') as f:
        myDataList = f.readlines()
        
    for line in myDataList:
        entry = line.strip().split(',')
        if len(entry) >= 3:
            if entry[2] == dateString:
                marked_today_set.add(entry[0])
    print(f"Loaded attendance for today: {marked_today_set}")

def markAttendance(name):
    file_path = 'Attendance.csv'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write('Name,Time,Date\n')

    now = datetime.now()
    dtString = now.strftime('%H:%M:%S')
    dateString = now.strftime('%Y-%m-%d')
    
    with open(file_path, 'a') as f:
        f.write(f'{name},{dtString},{dateString}\n')
    
    if name not in marked_today_set:
        marked_today_set.add(name)
        print(f"Attendance Marked: {name}")
        speak(f"Welcome {name}")
    else:
        print(f"Logging: {name} at {dtString}")

def register_new_user(img, path):
    
    root = tk.Tk()
    root.withdraw()
    
    # Ask for the name
    name = simpledialog.askstring("Register New User", "Enter Name:")
    root.destroy()
    
    if name:
        # Save the image
        filename = f"{path}/{name}.jpg"
        cv2.imwrite(filename, img)
        print(f"User {name} registered successfully!")
        speak(f"Registered {name}")
        return True
    return False

load_today_attendance()


cap = cv2.VideoCapture(0)
print("Attendance system started. Using basic face detection (no recognition model).")
print("Press 'q' to quit, 'r' to register a new user")

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image from camera. Please check camera permissions.")
        break

    
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(img, "Face Detected", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        
        markAttendance("UnidentifiedFace")
    
    cv2.imshow('Attendance System (Face Detection Mode)', img)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        speak("Please look at the camera for registration")
        success, clean_img = cap.read()
        if success:
            clean_img = cv2.flip(clean_img, 1)
            if register_new_user(clean_img, path):
                print("New user registered!")

cap.release()
cv2.destroyAllWindows()
