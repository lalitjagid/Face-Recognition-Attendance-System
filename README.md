# Face Recognition Attendance System

A Python-based Face Recognition Attendance System that uses Flask, OpenCV, SQLite, HTML and CSS to register students and mark their attendance using face recognition.

## 📌 Project Overview

The Face Recognition Attendance System is designed to make student attendance easier and more automated.

The system allows an administrator to:

- Register students
- Capture a student's face
- Train the face recognition model
- Recognize registered students
- Mark attendance automatically
- View attendance records
- Manage student information
- Check attendance percentage

## 🚀 Features

### 👨‍🎓 Student Management
- Register new students
- Store student ID, name, roll number and course
- View registered students
- Edit student information
- Delete student information
- View individual student profiles

### 📸 Face Registration
- Capture a student's face using the camera
- Detect the face using OpenCV Haar Cascade
- Save the processed face image
- One face image is used for each student

### 🤖 Face Recognition
- Uses OpenCV for face detection
- Uses LBPH Face Recognizer for recognition
- Matches the captured face with registered students

### 📅 Attendance Management
- Automatically marks attendance after successful face recognition
- Prevents duplicate attendance for the same student on the same day
- Stores attendance date and time
- Shows attendance records
- Calculates attendance percentage

### 🔐 Admin System
- Admin login
- Dashboard
- Student management
- Attendance management

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Backend programming |
| Flask | Web framework |
| OpenCV | Face detection and recognition |
| SQLite | Database |
| HTML | Web page structure |
| CSS | Web page design |
| Jinja2 | Dynamic HTML templates |

## 📁 Project Structure

```text
Face-Recognition-Attendance-System/
│
├── app.py
├── database.py
├── face_capture.py
├── face_recognition.py
├── face_test.py
├── train.py
├── attendance.py
├── camera_test.py
├── requirements.txt
├── haarcascade_frontalface_default.xml
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── success.html
│   ├── camera.html
│   ├── attendance_camera.html
│   ├── dashboard.html
│   ├── students.html
│   ├── student_profile.html
│   ├── edit_student.html
│   └── attendance.html
│
└── static/
    └── style.css
