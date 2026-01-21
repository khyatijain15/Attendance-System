import cv2
import numpy as np
# pip install face-recognition 
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    print("Warning: face_recognition module not available. Using basic face detection instead.")
    FACE_RECOGNITION_AVAILABLE = False
 
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

import os
from datetime import datetime
import pyttsx3
import tkinter as tk
from tkinter import simpledialog
from flask_dashboard import dashboard_data, start_dashboard_server
import threading

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()


# The path where faces images are stored.

path = 'EmployeesFaces'  
if not os.path.exists(path):
    os.makedirs(path)

images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    print(classNames)
 
def findEncodings(images):
    if not FACE_RECOGNITION_AVAILABLE:
        return []  
    
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            print(f"No face found in one of the images.")
    return encodeList
 

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
            # entry[0] is Name, entry[2] is Date
            if entry[2] == dateString:
                marked_today_set.add(entry[0])
    print(f"Loaded attendance for today: {marked_today_set}")

def markAttendance(name):
    file_path = 'Attendance.csv'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write('Name,Time,Date\n')

   
    if name not in marked_today_set:
        now = datetime.now()
        dtString = now.strftime('%H:%M:%S')
        dateString = now.strftime('%Y-%m-%d')
        
        with open(file_path, 'a') as f:
            f.write(f'{name},{dtString},{dateString}\n')
        
        marked_today_set.add(name)
        print(f"Attendance Marked: {name}")
        speak(f"Welcome {name}")
    else:
        # Person already marked today
        print(f"{name} already marked today")

def register_new_user(img, path):
   
    root = tk.Tk()
    root.withdraw()
    
   
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

encodeListKnown = findEncodings(images)
print(f'Encoding Complete. Found {len(encodeListKnown)} known faces.')
load_today_attendance()

try:
    start_dashboard_server(port=5001)
    print("✓ Dashboard available at: http://127.0.0.1:5001")
except Exception as e:
    print(f"⚠ Dashboard could not be started: {e}")

if not FACE_RECOGNITION_AVAILABLE:
    print("Using basic face detection mode (Haar Cascade)")
else:
    print("Using advanced face recognition mode")


cap = cv2.VideoCapture(0)

if not FACE_RECOGNITION_AVAILABLE:
    
    print("Starting camera in basic detection mode...")
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture image from camera. Please check camera permissions.")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        detected_this_frame = set()
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.rectangle(img, (x, y+h-35), (x+w, y+h), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, "Detected", (x+6, y+h-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            detected_this_frame.add("DetectedFace")
            markAttendance("DetectedFace")

        
        dashboard_data.update_frame(img)
        dashboard_data.update_active_users(detected_this_frame)

        cv2.imshow('Webcam - Face Detection Mode', img)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            speak("Please look at the camera for registration")
            success, clean_img = cap.read()
            if success:
                if register_new_user(clean_img, path):
                    images = []
                    classNames = []
                    myList = os.listdir(path)
                    for cl in myList:
                        curImg = cv2.imread(f'{path}/{cl}')
                        images.append(curImg)
                        classNames.append(os.path.splitext(cl)[0])
                    encodeListKnown = findEncodings(images)
                    print("Database updated!")

else:

    print("Starting camera in face recognition mode...")
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture image from camera. Please check camera permissions.")
            break

        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

        detected_this_frame = set()
        name = "Unknown"
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            if len(encodeListKnown) > 0:
                matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            
                matchIndex = np.argmin(faceDis)
                
                if faceDis[matchIndex]< 0.50:
                    name = classNames[matchIndex].upper()
                    markAttendance(name)
                    detected_this_frame.add(name)
                else: name = 'Unknown'
            else:
                name = 'Unknown'
                
            
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            
            # Color coding: Green for present, Red for unknown
            if name != "Unknown":
                color = (0, 255, 0) # Green
                cv2.putText(img, "Marked", (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7, color, 2)
            else:
                color = (0, 0, 255) # Red

            cv2.rectangle(img,(x1,y1),(x2,y2),color,2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),color,cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        
        # Update dashboard data
        dashboard_data.update_frame(img)
        dashboard_data.update_active_users(detected_this_frame)
        
        cv2.imshow('Webcam',img)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            speak("Please look at the camera for registration")
            
            success, clean_img = cap.read()
            if success:
                if register_new_user(clean_img, path):
                    # Reload known faces
                    images = []
                    classNames = []
                    myList = os.listdir(path)
                    for cl in myList:
                        curImg = cv2.imread(f'{path}/{cl}')
                        images.append(curImg)
                        classNames.append(os.path.splitext(cl)[0])
                    encodeListKnown = findEncodings(images)
                    print("Database updated!")

cap.release()
cv2.destroyAllWindows()
