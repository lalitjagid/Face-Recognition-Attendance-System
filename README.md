<div align="center">

# 🚀 Face Recognition Attendance System

### Smart • Automated • Efficient

A Python-based attendance management application that uses facial recognition to simplify student attendance tracking.

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
</p>

[Features](#-features) •
[Technologies](#-technologies-used) •
[Installation](#-installation) •
[Project Structure](#-project-structure) •
[Developer](#-developer)

</div>

---

## 📌 About the Project

The **Face Recognition Attendance System** is a Python-based web application developed to make student attendance management easier, faster, and more efficient.

The application uses OpenCV for face detection and recognition, Flask for the web interface, and SQLite for storing student and attendance information.

It provides an interface for administrators to register students, capture facial images, recognize registered students, manage attendance records, and view attendance percentages.

## ✨ Features

### 👨‍🎓 Student Management
- Register new students.
- Store student ID, name, roll number, and course.
- View the registered student list.
- Edit student information.
- Delete student records.
- View individual student profiles.

### 📸 Face Registration
- Capture student face images using a camera.
- Detect faces using OpenCV Haar Cascade.
- Process and save facial images.
- Associate captured images with registered students.

### 🤖 Face Recognition
- Detect faces using OpenCV.
- Recognize faces using the LBPH Face Recognizer.
- Match detected faces against the trained model.
- Identify registered students for attendance marking.

### 📅 Attendance Management
- Mark attendance after successful face recognition.
- Prevent duplicate attendance entries for the same student on the same day.
- Store attendance dates and times.
- View attendance records.
- Calculate student attendance percentages.

### 🔐 Admin Dashboard
- Admin login.
- Dashboard for attendance management.
- Student record management.
- Attendance record viewing.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| OpenCV | Face detection and recognition |
| LBPH | Face recognition algorithm |
| SQLite | Database management |
| HTML5 | Web page structure |
| CSS3 | User interface styling |
| Jinja2 | Dynamic HTML templates |

## 🖥️ Application Workflow

```text
        Student Registration
                 |
                 v
         Capture Face Image
                 |
                 v
          Train the Model
                 |
                 v
        Recognize Student
                 |
                 v
       Verify Recognition
                 |
                 v
        Mark Attendance
                 |
                 v
      Store Data in SQLite
                 |
                 v
      View Attendance Records
```

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
```

## ⚙️ Installation

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/lalitjagid/Face-Recognition-Attendance-System.git
```

### 2. Open the Project Directory

```bash
cd Face-Recognition-Attendance-System
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

If `app.py` is the main Flask entry point, run:

```bash
python app.py
```

Open the local address displayed in the terminal in your web browser.

> **Note:** Camera access, database initialization, and face recognition dependencies must be configured correctly for the application to work.

## 🎯 Project Objectives

- Automate student attendance management.
- Reduce manual attendance-taking effort.
- Maintain organized student and attendance records.
- Apply computer vision to a practical problem.
- Develop hands-on experience with Python web development.

## 🔮 Future Improvements

- Export attendance records to CSV or Excel.
- Add date-wise attendance reports.
- Improve face recognition accuracy.
- Add more detailed attendance analytics.
- Improve security and authentication.
- Enhance the user interface and responsiveness.

## 👨‍💻 Developer

<div align="center">

### Lalit Jangid

**BCA Student | Aspiring Software Developer**

Interested in Python, Java, Web Development, and practical software projects.

<a href="https://github.com/lalitjagid">
  <img src="https://img.shields.io/badge/GitHub-Visit%20My%20Profile-181717?style=for-the-badge&logo=github" alt="GitHub Profile">
</a>

</div>

---

<div align="center">

**Built with Python and OpenCV ❤️**

⭐ If you find this project interesting, consider giving the repository a star!

</div>
